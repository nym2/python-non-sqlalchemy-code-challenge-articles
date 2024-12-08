class Article:
    all = []  # Class attribute to store all articles

    def __init__(self, author, magazine, title):
        # Validations
        if not isinstance(author, Author):
            raise Exception("Author must be an instance of the Author class.")
        if not isinstance(magazine, Magazine):
            raise Exception("Magazine must be an instance of the Magazine class.")
        if not isinstance(title, str) or not (5 <= len(title) <= 50):
            raise Exception("Title must be a string between 5 and 50 characters.")
        
        self._author = author
        self._magazine = magazine
        self._title = title

        # Add to class-level list of articles
        Article.all.append(self)

        # Add the article to the magazine's articles list
        magazine.add_article(self)
        
        # Add article to author's articles list
        author.add_article(self)

    @property
    def title(self):
        return self._title

    @property
    def author(self):
        return self._author

    @property
    def magazine(self):
        return self._magazine


class Author:
    def __init__(self, name):
        # Ensure name is a non-empty string
        if not isinstance(name, str) or not name:
            raise ValueError("Name must be a non-empty string.")
        self._name = name
        self._articles = []

    @property
    def name(self):
        return self._name

    def articles(self):
        return self._articles

    def magazines(self):
        # Return a list of unique magazines associated with the author's articles
        return list({article.magazine for article in self._articles})

    def add_article(self, article):
        # Add a new article and associate it with the author
        self._articles.append(article)

    def topic_areas(self):
        # Return a list of unique topic areas for the author's articles
        if not self._articles:
            return None
        return list({article.magazine.category for article in self._articles})


class Magazine:
    all = []

    def __init__(self, name, category):
        if not isinstance(name, str) or len(name) < 2 or len(name) > 16:
            raise Exception("Invalid name length")
        if not isinstance(category, str) or len(category) == 0:
            raise Exception("Category cannot be empty")
        
        self.name = name
        self.category = category
        self._articles = []
        Magazine.all.append(self)

    def articles(self):
        return self._articles

    def contributors(self):
        contributors = set(article.author for article in self._articles)
        return list(contributors)

    def article_titles(self):
        return [article.title for article in self._articles] if self._articles else None

    def add_article(self, article):
        self._articles.append(article)

    def contributing_authors(self):
        author_count = {}
        for article in self._articles:
            if article.author not in author_count:
                author_count[article.author] = 0
            author_count[article.author] += 1
        
        contributing_authors = [author for author, count in author_count.items() if count > 2]
        return contributing_authors if contributing_authors else None

    @classmethod
    def top_publisher(cls):
        if not cls.all:
            return None

        magazine_article_count = {magazine: len(magazine.articles()) for magazine in cls.all}
        max_articles = max(magazine_article_count.values(), default=0)

        if max_articles == 0:
            return None

        top_magazines = [magazine for magazine, count in magazine_article_count.items() if count == max_articles]
        return top_magazines[0] if top_magazines else None
