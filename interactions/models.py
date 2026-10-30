from django.conf import settings
from django.db import models


class Comment(models.Model):
    blog = models.ForeignKey(
        'blogs.BlogPost',
        on_delete=models.CASCADE,
        related_name='comments'
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments'
    )

    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user.username}'


class Like(models.Model):
    blog = models.ForeignKey(
        'blogs.BlogPost',
        on_delete=models.CASCADE,
        related_name='likes'
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='likes'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['blog', 'user'],
                name='unique_blog_like_per_user'
            )
        ]

    def __str__(self):
        return f'{self.user.username} liked {self.blog.title}'
