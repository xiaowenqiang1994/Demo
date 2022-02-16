from django.db import models
from user.models import User

# Create your models here.

class Post(models.Model):
    uid = models.IntegerField()
    title = models.CharField(max_length=64)
    content = models.TextField()
    create = models.DateTimeField(auto_now_add=True)

    @property
    def auth(self):
        if not hasattr(self, '_auth'):
            self._auth = User.objects.get(id=self.uid)
            return self._auth

    def comments(self):
        return Comment.objects.filter(pid=self.id)

    def tags(self):
        post_tag_relations = PostTags.objects.filter(pid=self.id).only('id')
        tag_id_list = [pt.id for pt in post_tag_relations]
        return Tag.objects.filter(id__in=tag_id_list)

    def delete(self):
        from post.helper import rds
        rds.zrem('ReadRank', self.id)
        self.comments().delete()
        PostTags.objects.filter(pid=self.id).delete()
        super().delete()



class Comment(models.Model):
    pid = models.IntegerField()
    name = models.CharField(max_length=64)
    content = models.TextField()
    create = models.DateTimeField(auto_now_add=True)

    @property
    def post(self):
        if not hasattr(self, '_post'):
            self._post = Post.objects.filter(id=self.pid)
        return self._post


class Tag(models.Model):
    name = models.CharField(max_length=64, unique=True)

    @classmethod
    def ensure_tags(cls, tag_names):
        '''确保 Tags 存在'''
        tags = Tag.objects.filter(name=tag_names)
        new_name = set(tag_names) - set(tag.name for tag in tags)
        Tag.objects.bulk_create([Tag(name=n) for n in new_name])
        return Tag.objects.filter(name=tag_names)

    def posts(self):
        post_id = [pt.id for pt in PostTags.objects.filter(tid=self.id).only('id')]
        return Post.objects.filter(id__in=post_id)


class PostTags(models.Model):
    pid = models.IntegerField()
    tid = models.IntegerField()

    @classmethod
    def update_post_tags(cls, post_id, tag_names):
        tags = Tag.ensure_tags(tag_names)
        tid_list = [tag.id for tag in tags]
        # 取出旧的关系
        post_tags = cls.objects.filter(pid=post_id)
        # 删除不在需要的 Tag 关系
        for pt in post_tags:
            if pt.id not in tid_list:
                pt.delete()
        new_post_tag_ids = set(tid_list) - set(pt.id for pt in post_tags)
        new_post_tags = [PostTags(pid=post_id, tid=tid) for tid in new_post_tag_ids]
        return cls.objects.bulk_create(new_post_tags)









