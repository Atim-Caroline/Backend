from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from .models import ContentRule, ComplianceCheck, ComplianceReport
from .serializers import ContentRuleSerializer, ComplianceCheckSerializer, ComplianceReportSerializer
import re
from textblob import TextBlob
from better_profanity import profanity

class ContentRuleViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ContentRuleSerializer
    queryset = ContentRule.objects.all()

class ComplianceCheckViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ComplianceCheckSerializer

    def get_queryset(self):
        return ComplianceCheck.objects.filter(post__account__user=self.request.user)

    @action(detail=False, methods=['post'])
    def check_content(self, request):
        content = request.data.get('content')
        if not content:
            return Response(
                {'error': 'Content is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        results = []
        active_rules = ContentRule.objects.filter(is_active=True)

        for rule in active_rules:
            check_result = {
                'rule': rule.name,
                'type': rule.rule_type,
                'passed': True,
                'details': {}
            }

            if rule.rule_type == 'keyword':
                keywords = rule.pattern.split(',')
                found_keywords = [k for k in keywords if k.strip().lower() in content.lower()]
                check_result['passed'] = len(found_keywords) == 0
                check_result['details']['found_keywords'] = found_keywords

            elif rule.rule_type == 'regex':
                matches = re.findall(rule.pattern, content)
                check_result['passed'] = len(matches) == 0
                check_result['details']['matches'] = matches

            elif rule.rule_type == 'sentiment':
                blob = TextBlob(content)
                sentiment = blob.sentiment.polarity
                check_result['passed'] = sentiment >= 0
                check_result['details']['sentiment_score'] = sentiment

            elif rule.rule_type == 'profanity':
                has_profanity = profanity.contains_profanity(content)
                check_result['passed'] = not has_profanity
                check_result['details']['has_profanity'] = has_profanity

            results.append(check_result)

        return Response(results)

class ComplianceReportViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ComplianceReportSerializer

    def get_queryset(self):
        return ComplianceReport.objects.filter(post__account__user=self.request.user)

    @action(detail=True, methods=['get'])
    def summary(self, request, pk=None):
        report = self.get_object()
        summary_data = {
            'post_id': report.post.id,
            'overall_status': report.overall_status,
            'failed_rules_count': report.failed_rules.count(),
            'failed_rules': list(report.failed_rules.values('name', 'rule_type', 'severity')),
            'created_at': report.created_at,
            'report_data': report.report_data
        }
        return Response(summary_data) 