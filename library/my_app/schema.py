import graphene

from graphene_django.types import DjangoObjectType, ObjectType
from .models import Author, Book, Reader, Rent
from django.utils import timezone


class AuthorType(DjangoObjectType):
    class Meta:
        model = Author


class BookType(DjangoObjectType):
    class Meta:
        model = Book


class ReaderType(DjangoObjectType):
    class Meta:
        model = Reader


class RentType(DjangoObjectType):
    class Meta:
        model = Rent


class Query(ObjectType):
    get_book = graphene.Field(BookType, id=graphene.Int())
    get_author = graphene.Field(AuthorType, id=graphene.Int())
    get_reader = graphene.Field(ReaderType, id=graphene.Int())
    books = graphene.List(BookType)
    authors = graphene.List(AuthorType)
    rents = graphene.List(RentType, id=graphene.Int())

    def resolve_get_book(self, input, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return Book.objects.get(id=id)

        return None

    def resolve_get_author(self, input, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return Author.objects.get(id=id)

        return None

    def resolve_get_reader(self, input, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return Reader.objects.get(id=id)

        return None

    def resolve_books(self, info, **kwargs):
        return Book.objects.all()

    def resolve_authors(self, info, **kwargs):
        return Author.objects.all()

    def resolve_rents(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return Reader.objects.get(id=id).rent

        return None


class AuthorInput(graphene.InputObjectType):
    id = graphene.ID()
    name = graphene.String()
    foto = graphene.String()
    birth = graphene.Date()
    death = graphene.Date()
    books = graphene.List(BookType)
    available = graphene.List(BookType)


class BookInput(graphene.InputObjectType):
    id = graphene.ID()
    name = graphene.String()
    max_dur = graphene.Int()
    cover = graphene.String()
    author = graphene.Field(AuthorType)


class ReaderInput(graphene.InputObjectType):
    id = graphene.ID()
    name = graphene.String()
    mail = graphene.String()
    rent = graphene.List(BookType)
    fine = graphene.Int()


class RentInput(graphene.InputObjectType):
    id = graphene.ID()
    book = graphene.Field(BookType)
    reader = graphene.Field(ReaderType)
    time = graphene.Date()
    dur = graphene.Int()
    fpd = graphene.Int()


class CreateBook(graphene.Mutation):
    class Arguments:
        input = BookInput(required=True)

    ok = graphene.Boolean()
    book = graphene.Field(BookType)

    @staticmethod
    def mutate(root, info, input=None):
        ok = True
        book_instance = Book(name=input.name, max_dur=input.max_dur, cover=input.cover,
                             author=Author.objects.get(id=input.author.id))
        book_instance.save()
        return CreateBook(ok=ok, book=book_instance)


class UpdateBook(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        input = BookInput(required=True)

    ok = graphene.Boolean()
    book = graphene.Field(BookType)

    @staticmethod
    def mutate(root, info, id, input=None):
        ok = False
        book_instance = Book.objects.get(id=id)
        if book_instance:
            ok = True
            author = Author.objects.get(id=input.author.id)
            book_instance = Book(name=input.name, max_dur=input.max_dur, cover=input.cover, author=author)
            book_instance.save()
            return UpdateBook(ok=ok, book=book_instance)
        return UpdateBook(ok=ok, book=None)


class DeleteBook(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        input = BookInput(required=True)

    ok = graphene.Boolean()
    book = graphene.Field(BookType)

    @staticmethod
    def mutate(root, info, id, input=None):
        ok = False
        book_instance = Book.objects.get(id=id)
        if book_instance:
            ok = True
            book_instance.delete()
            return DeleteBook(ok=ok)
        return DeleteBook(ok=ok)


class CreateReader(graphene.Mutation):
    class Arguments:
        input = ReaderInput(required=True)

    ok = graphene.Boolean()
    book = graphene.Field(ReaderType)

    @staticmethod
    def mutate(root, info, input=None):
        ok = True
        reader_instance = Reader(name=input.name, mail=input.mail, rent=[],
                             fine=0)
        reader_instance.save()
        return CreateReader(ok=ok, reader=reader_instance)


class UpdateReader(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        input = ReaderInput(required=True)

    ok = graphene.Boolean()
    reader = graphene.Field(ReaderType)

    @staticmethod
    def mutate(root, info, id, input=None):
        ok = False
        reader_instance = Reader.objects.get(id=id)
        if reader_instance:
            ok = True
            reader_instance = Reader(name=input.name, mail=input.mail, rent=input.rent, fine=input.fine)
            reader_instance.save()
            return UpdateReader(ok=ok, reader=reader_instance)
        return UpdateReader(ok=ok, reader=None)


class DeleteReader(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        input = ReaderInput(required=True)

    ok = graphene.Boolean()
    reader = graphene.Field(ReaderType)

    @staticmethod
    def mutate(root, info, id, input=None):
        ok = False
        reader_instance = Reader.objects.get(id=id)
        if reader_instance:
            ok = True
            reader_instance.delete()
            return DeleteReader(ok=ok)
        return DeleteReader(ok=ok)


class CreateAuthor(graphene.Mutation):
    class Arguments:
        input = AuthorInput(required=True)

    ok = graphene.Boolean()
    author = graphene.Field(AuthorType)

    @staticmethod
    def mutate(root, info, input=None):
        ok = True
        author_instance = Author(name=input.name, foto=input.foto, birth=input.birth,
                             death=input.death, books=[], available=[])
        author_instance.save()
        return CreateAuthor(ok=ok, author=author_instance)


class UpdateAuthor(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        input = AuthorInput(required=True)

    ok = graphene.Boolean()
    author = graphene.Field(AuthorType)

    @staticmethod
    def mutate(root, info, id, input=None):
        ok = False
        author_instance = Author.objects.get(id=id)
        if author_instance:
            ok = True
            available = []
            for i in Book.objects.filter(author=author_instance):
                if Rent.objects.filter(book=i) == None:
                    available.append(i)
            author_instance = Author(name=input.name, foto=input.foto, birth=input.birth,
                             death=input.death)
            author_instance.save()
            author_instance.books.set(Book.objects.filter(author=author_instance))
            author_instance.available.set(available)
            return UpdateAuthor(ok=ok, author=author_instance)
        return UpdateAuthor(ok=ok, author=None)


class DeleteAuthor(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        input = AuthorInput(required=True)

    ok = graphene.Boolean()
    author = graphene.Field(AuthorType)

    @staticmethod
    def mutate(root, info, id, input=None):
        ok = False
        author_instance = Author.objects.get(id=id)
        if author_instance:
            ok = True
            author_instance.delete()
            return DeleteAuthor(ok=ok)
        return DeleteAuthor(ok=ok)


class rentBook(graphene.Mutation):
    class Arguments:
        id=graphene.Int(required=True)
        input=RentInput(required=True)

    ok = graphene.Boolean()
    rent = graphene.Field(RentType)

    @staticmethod
    def mutate(root, info, input=None):
        ok=True
        rent_instance = Rent(book=input.book, reader=input.reader, dur=input.book.max_dur, fpd=input.fpd)
        Reader.objects.get(id=input.reader.id).rent.append(rent_instance)
        rent_instance.save()
        Reader.objects.get(id=input.reader.id).save()
        return rentBook(ok=ok, rent=rent_instance)


class returnBook(graphene.Mutation):
    class Arguments:
        id=graphene.Int(required=True)
        input=RentInput(required=True)

    ok = graphene.Boolean()
    rent=graphene.Field(RentType)

    @staticmethod
    def mutate(root, info, id, input=None):
        ok=False
        rent_instance = Rent.objects.get(id=id)
        if rent_instance:
            ok=True
            reader = Reader.objects.get(id=input.reader.id)
            if rent_instance.time.days + rent_instance.dur<timezone.now().days:
                reader.fine += input.fpd*(timezone.now().days-rent_instance.time.days-rent_instance.dur)
            reader.rent.remove(rent_instance)
            rent_instance.delete()
            return returnBook(ok=ok)
        return returnBook(ok=ok)


class Mutation(graphene.ObjectType):
    create_book = CreateBook.Field()
    create_author = CreateAuthor.Field()
    create_reader = CreateReader.Field()
    update_book = UpdateBook.Field()
    update_author = UpdateAuthor.Field()
    update_reader = UpdateReader.Field()
    delete_book = DeleteBook.Field()
    delete_author = DeleteAuthor.Field()
    delete_reader = DeleteReader.Field()
    rent_book = rentBook.Field()
    return_book = returnBook.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)
