from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Integer, ForeignKey, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, UTC, timezone

db = SQLAlchemy()

class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    posts = relationship("Post", back_populates="user", cascade="all, delete")
    comments = relationship("Comment", back_populates="user", cascade="all, delete")
    likes = relationship("Like", back_populates="user", cascade="all, delete")

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "username": self.username,
            "created_at": self.created_at.isoformat()
            # do not serialize the password, its a security breach
        }

class Post(db.Model):
   id: Mapped[int] = mapped_column(primary_key=True)
   user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
   image_url: Mapped[str] = mapped_column(String(255),nullable=False)
   caption: Mapped[str] = mapped_column(Text, nullable=True)
   created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

   user = relationship("User", back_populates="posts")
   comments = relationship("comment", back_populates="post", cascade="all, delete")
   likes = relationship("Like", back_populates="post", cascade="all, delete")

   def serialize(self):
      return{
         "id": self.id,
         "user_id": self.user_id,
         "image_url": self.image.url,
         "caption": self.caption,
         "created_at": self.created_at.isoformat(),
      }
   
   class Comment(db.Model):
      id: Mapped[int] = mapped_column(primary_key=True)
      user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
      post_id: Mapped[int] = mapped_column(ForeignKey("post.id"), nullable=False)
      text: Mapped[str] = mapped_column(Text, nullable=False)
      created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

      user = relationship("User", back_populates="comments")
      post = relationship("Post", back_populates="comments")

      def serialize(self):
         return{
            "id": self.id,
            "user_id": self.user_id,
            "post_id": self.post_id,
            "text": self.text,
            "created_at": self.created_at.isoformat(),
         }
      
      class Like(db.Model):
         id: Mapped[int] = mapped_column(primary_key=True)
         user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
         post_id: Mapped[int] = mapped_column(ForeignKey("post.id"), nullable=False)
         created_at: Mapped[datetime]= mapped_column(DateTime, default=datetime.utcnow)

      user = relationship("User", back_populates="likes")
      post = relationship("Post", back_populates="likes")
       
      def serialize(self):
          return{
            "id": self.id,
            "user_id": self.user_id,
            "post_id": self.post_id,
            "created_at": self.created_at.isoformat(),
         }
         