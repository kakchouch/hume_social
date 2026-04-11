from django.contrib import admin
from .models import MiniThesis, Comment, Citation


@admin.register(MiniThesis)
class MiniThesisAdmin(admin.ModelAdmin):
    """Admin for mini-theses."""

    list_display = (
        "id",
        "author",
        "thesis_truncated",
        "rigor_score",
        "comment_count",
        "created_at",
        "is_published",
    )
    list_filter = ("is_published", "is_featured", "created_at")
    search_fields = ("author__username", "thesis", "conclusion")
    readonly_fields = ("rigor_score", "comment_count", "citation_count")

    def thesis_truncated(self, obj):
        return obj.thesis[:50] + "..." if len(obj.thesis) > 50 else obj.thesis

    thesis_truncated.short_description = "Thesis"


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Admin for comments."""

    list_display = (
        "id",
        "author",
        "thesis_truncated",
        "content_truncated",
        "created_at",
    )
    list_filter = ("created_at",)
    search_fields = ("author__username", "content")

    def thesis_truncated(self, obj):
        return (
            obj.thesis.thesis[:30] + "..."
            if len(obj.thesis.thesis) > 30
            else obj.thesis.thesis
        )

    def content_truncated(self, obj):
        return obj.content[:50] + "..." if len(obj.content) > 50 else obj.content


@admin.register(Citation)
class CitationAdmin(admin.ModelAdmin):
    """Admin for citations."""

    list_display = (
        "id",
        "citing_thesis_truncated",
        "cited_thesis_truncated",
        "context_truncated",
    )
    search_fields = ("citing_thesis__thesis", "cited_thesis__thesis")

    def citing_thesis_truncated(self, obj):
        return obj.citing_thesis.thesis[:30] + "..."

    citing_thesis_truncated.short_description = "Citing Thesis"

    def cited_thesis_truncated(self, obj):
        return obj.cited_thesis.thesis[:30] + "..."

    cited_thesis_truncated.short_description = "Cited Thesis"

    def context_truncated(self, obj):
        return obj.context[:50] + "..." if len(obj.context) > 50 else obj.context
