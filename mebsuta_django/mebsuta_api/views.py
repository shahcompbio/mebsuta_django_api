from django.contrib.auth.models import User, Group
from rest_framework import viewsets, permissions, filters

from .serializers import UserSerializer, GroupSerializer, AnnotationRollUpSerializer, AnnotationDebrisRollUpSerializer, Cell_ImageSerializer, CellSerializer, AnnotationSerializer, Mebsuta_UsersSerializer, DebrisSerializer, LibrarySerializer, CellsAnnotationSerializer
from .models import Cell_Image, Debris, Library, Annotation, Mebsuta_Users
from rest_framework.response import Response
from rest_framework.parsers import JSONParser

from .functions import dictfetchall
import itertools

from django.db.models import Count, Q, Max, Sum, OuterRef, Subquery
from django.db import connection
from django_filters.rest_framework import DjangoFilterBackend
'''

from django.db.models import Count, Q, Max, Sum, OuterRef, Subquery
from django.db import connection
from mebsuta_api.functions import dictfetchall
from mebsuta_api.serializers import LibrarySerializer
from rest_framework.response import Response


'''


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class Cell_ImageViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Cell Images to be viewed or edited.
    """
    queryset = Cell_Image.objects.all()
    serializer_class = Cell_ImageSerializer
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = ["cell_id", "library_id"]
    ordering_fields = ["cell_id", "library_id"]
    permission_classes = [permissions.IsAuthenticated]


class CellsViewSet(viewsets.ModelViewSet):
    queryset = Cell_Image.objects.all()
    serializer_class = CellSerializer
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = ["cell_id", "library_id", 'row', 'col']
    ordering_fields = ["cell_id", ]
    permission_classes = [permissions.IsAuthenticated]


class DebrisViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Debris to be viewed or edited.
    """
    queryset = Debris.objects.all()
    serializer_class = DebrisSerializer
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = ["cell_id", "library_id", "user_id", "isDebris"]
    ordering_fields = ["cell_id", "library_id"]
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request):
        user = request.data["data"]["user_id"]
        row = request.data["data"]["row"]
        col = request.data["data"]["col"]
        library_id = request.data["data"]["library_id"]
        isDebris = request.data["data"]["isDebris"]
        cell_id = request.data["data"]["cell_id"]

        ref_user = Mebsuta_Users.objects.get(user_id=user)
        ref_cell = Cell_Image.objects.get(
            library_id=library_id, cell_id=cell_id)

        obj, created = Debris.objects.update_or_create(
            user=ref_user, row=row, col=col, Cell_Image=ref_cell, library_id=library_id, cell_id=cell_id,
            defaults={'isDebris': isDebris}
        )
        print(obj, created)
        return Response({'received data': request.data})


class AnnotationsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Annotations to be viewed or edited.
    """
    queryset = Annotation.objects.all()
    serializer_class = AnnotationSerializer
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = ["cell_id", "library_id", "user_id", "annotation"]
    ordering_fields = ["cell_id", "library_id"]
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request):
        '''
        1. get request data
        2. row col annotaiton user id, library id, cell image its attached to
        3. retrieve user_id and cell_image object
        4. tie annotation to it
        5. create
        '''
        print(request.data["data"])
        user = request.data["data"]["user_id"]
        row = request.data["data"]["row"]
        col = request.data["data"]["col"]
        library_id = request.data["data"]["library_id"]
        annotation = request.data["data"]["annotation"]
        cell_id = request.data["data"]["cell_id"]

        ref_user = Mebsuta_Users.objects.get(user_id=user)
        ref_cell = Cell_Image.objects.get(
            library_id=library_id, cell_id=cell_id)
        if annotation == "":
            delete_anno = Annotation.objects.get(
                user_id=user, row=row, col=col, library_id=library_id, Cell_Image=ref_cell)
            delete_anno.delete()
            print("null annotation, deleted Annotation")
        else:
            obj, created = Annotation.objects.update_or_create(
                user=ref_user, row=row, col=col, Cell_Image=ref_cell, library_id=library_id, cell_id=cell_id,
                defaults={'annotation': annotation}
            )
            print(obj, created)
        return Response({'received data': request.data})


class CellsAnnotations(viewsets.ModelViewSet):
    serializer_class = CellsAnnotationSerializer

    def get_queryset(self):
        if "user_id" in self.request.GET and "library_id" in self.request.GET:
            current_library = self.request.GET["library_id"]
            current_user = self.request.GET["user_id"]
            result = Annotation.objects.filter(
                library_id=current_library, user_id=current_user).order_by('cell_id')
            return result
        elif "user_id" not in self.request.GET and "library_id" in self.request.GET:
            current_library = self.request.GET["library_id"]

            most_freq_anno_subq = Subquery(Annotation.objects.filter(library_id=current_library, cell_id=OuterRef("cell_id"))
                                           .values('annotation').annotate(count=Count('annotation')).order_by('-count').values('annotation')[:1])

            result = Annotation.objects.filter(library_id=current_library).values(
                'cell_id').distinct().annotate(annotation=most_freq_anno_subq).order_by('cell_id')
            return list(result)
        else:
            return Annotation.objects.all()


class Mebsuta_UsersViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Mebsuta Users to be viewed or edited.
    """
    queryset = Mebsuta_Users.objects.all()
    serializer_class = Mebsuta_UsersSerializer
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = ["user_id", "name"]
    permission_classes = [permissions.IsAuthenticated]


class LibraryViewSet(viewsets.ViewSet):
    """
    API endpoint that allows Libraries to be viewed or edited.
    """
    # modify get query set and check for user_id parameters lol
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        if "user_id" in self.request.GET:
            with connection.cursor() as c:
                c.execute('Select t1.library_id, t1.num_cells, IFNULL(t2.num_annotated, 0) num_annotated From (SELECT mebsuta_api_cell_image.library_id, COUNT(mebsuta_api_cell_image.library_id) AS num_cells FROM mebsuta_api_cell_image GROUP BY mebsuta_api_cell_image.library_id) t1 LEFT JOIN (SELECT mebsuta_api_annotation.library_id, count(mebsuta_api_annotation.id) as num_annotated FROM mebsuta_api_annotation WHERE mebsuta_api_annotation.user_id = %s GROUP BY mebsuta_api_annotation.library_id) t2 On t1.library_id = t2.library_id', [
                          self.request.GET["user_id"]])
                libraries = dictfetchall(c)

                serializer = LibrarySerializer(libraries, many=True)
                return Response(serializer.data)
        else:
            with connection.cursor() as c:
                c.execute('SELECT t1.library_id, t1.num_cells, t2.num_annotated FROM (SELECT mebsuta_api_cell_image.library_id, COUNT(mebsuta_api_cell_image.library_id) AS num_cells FROM mebsuta_api_cell_image GROUP BY mebsuta_api_cell_image.library_id) t1 INNER JOIN (SELECT mebsuta_api_cell_image.library_id, COUNT(DISTINCT mebsuta_api_annotation.cell_id) AS num_annotated FROM mebsuta_api_cell_image LEFT OUTER JOIN mebsuta_api_annotation ON (mebsuta_api_cell_image.id= mebsuta_api_annotation.Cell_Image_id) GROUP BY mebsuta_api_cell_image.library_id ) t2 on t1.library_id = t2.library_id')
                libraries = dictfetchall(c)

                serializer = LibrarySerializer(libraries, many=True)
                return Response(serializer.data)
class MasterCellsViewSet(viewsets.ModelViewSet):
    serializer_class = CellSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        if "user_id" in self.request.GET and "library_id" in self.request.GET:
            current_library = self.request.GET["library_id"]
            current_user = self.request.GET["user_id"]
            # get user annotations via subq and create a dictionary DO THIS IN SQL noob
            user_annos = Annotation.objects.filter(
                library_id=current_library, user_id=current_user).values("cell_id", "annotation").order_by('cell_id')
            anno_dict = {cell["cell_id"]: cell["annotation"]
                         for cell in user_annos}
            # get all cells from library
            full_library = Cell_Image.objects.filter(
                library_id=current_library).values('library_id', "cell_id", "row", "col", "annotation")
            # iterate through library of cells and check and match if cell_id in dictionary
            for cell in full_library:
                if cell["cell_id"] in anno_dict:
                    cell["annotation"] = anno_dict[cell["cell_id"]]

            return full_library
        elif "user_id" not in self.request.GET and "library_id" in self.request.GET:
            current_library = self.request.GET["library_id"]
            # get user blind annotations via subq and create a dictionary
            most_freq_anno_subq = Subquery(Annotation.objects.filter(library_id=current_library, cell_id=OuterRef("cell_id"))
                                           .values('annotation').annotate(count=Count('annotation')).order_by('-count').values('annotation')[:1])
            found_annos = Annotation.objects.filter(library_id=current_library).values(
                'cell_id').distinct().annotate(annotation=most_freq_anno_subq).order_by('cell_id')
            anno_dict = {cell["cell_id"]: cell["annotation"]
                         for cell in found_annos}
            # get all cells from library
            full_library = Cell_Image.objects.filter(
                library_id=current_library).values('library_id', "cell_id", "row", "col", "annotation")

            # iterate through library of cells and check and match if cell_id in dictionary
            for cell in full_library:
                if cell["cell_id"] in anno_dict:
                    cell["annotation"] = anno_dict[cell["cell_id"]]
            return full_library
        else:
            return Annotation.objects.all()


class CellDataViewSet(viewsets.ModelViewSet):
    serializer_class = Cell_ImageSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # whats going on here lads

        # we are only ever checking on user_id
        # library, row, col, userID

        if "user_id" in self.request.GET:
            curr_library = self.request.GET["library_id"]
            curr_row = self.request.GET["row"]
            curr_col = self.request.GET["col"]
            if len(curr_row) == 1:
                curr_row = "0" + curr_row
            if len(curr_col) == 1:
                curr_col = "0" + curr_col
            curr_cell_id = F"R{curr_row}_C{curr_col}"
            curr_user = Mebsuta_Users.objects.get(
                user_id=self.request.GET["user_id"])
            cells = Cell_Image.objects.filter(
                library_id=curr_library, cell_id=curr_cell_id)
            user_anno = Annotation.objects.filter(
                library_id=curr_library, cell_id=curr_cell_id, user=curr_user).first()
            user_isdebris = Debris.objects.filter(
                library_id=curr_library, cell_id=curr_cell_id, user=curr_user).first()
            for cell in cells:
                if user_anno:
                    print(user_anno.annotation)
                    cell.annotation = user_anno.annotation
                if user_isdebris:
                    print(user_isdebris.isDebris)
                    cell.isDebris = user_isdebris.isDebris
            return cells
        elif "user_id" not in self.request.GET and "library_id" in self.request.GET and "row" in self.request.GET and "col" in self.request.GET:
            curr_library = self.request.GET["library_id"]
            curr_row = self.request.GET["row"]
            curr_col = self.request.GET["col"]
            if len(curr_row) == 1:
                curr_row = "0" + curr_row
            if len(curr_col) == 1:
                curr_col = "0" + curr_col
            curr_cell_id = F"R{curr_row}_C{curr_col}"
            cells = Cell_Image.objects.filter(
                library_id=curr_library, cell_id=curr_cell_id)

            cell_anno = Annotation.objects.filter(library_id=curr_library, cell_id=curr_cell_id).values(
                'annotation').annotate(count=Count('annotation')).order_by('-count').values('annotation')[:1]
            cell_debris = Debris.objects.filter(library_id=curr_library, cell_id=curr_cell_id).values(
                'isDebris').annotate(count=Count('isDebris')).order_by('-count').values('isDebris')[:1]
            for cell in cells:
                if cell_anno.exists():
                    cell.annotation = cell_anno[0]["annotation"]
                if cell_debris.exists():
                    cell.isDebris = cell_debris[0]["isDebris"]
            return cells
        else:
            return Cell_Image.objects.all()


class TrialCellDataViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request):
        queryset = Cell_Image.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)


class AnnotationRollUpViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        annotated_list = list(Annotation.objects.values('library_id', 'user').order_by('library_id').annotate(
            Count('library_id'), Count('user')))

        iter_list = itertools.groupby(annotated_list, lambda x: x["library_id"])
        dict1 = [{"library_id": key, "user_count": [{'user': x["user"], 'num_annotated':x["user__count"]}
                                                    for x in group]}for key, group in iter_list]
        serializer = AnnotationRollUpSerializer(dict1, many=True)

        return Response(serializer.data)

class AnnotationDebrisRollUpViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]
    #
    # DEBRIS ONLY TRUE
    # c.execute(' Select t1.library_id, IFNULL(t2.num_debris, 0) num_debris FROM ( SELECT  DISTINCT mebsuta_api_cell_image.library_id FROM mebsuta_api_cell_image ORDER BY mebsuta_api_cell_image.library_id) t1 LEFT JOIN (SELECT mebsuta_api_debris.library_id, count(mebsuta_api_debris.id) as num_debris from mebsuta_api_debris where mebsuta_api_debris.isDebris = true GROUP BY mebsuta_api_debris.library_id) t2 on t1.library_id = t2.library_id')
    # but to be honest we want all debris whether true or false and its marked is what we want

    def list(self, request):
        with connection.cursor() as c:
            c.execute('Select t1.library_id, IFNULL(t2.total_debris, 0) total_debris , IFNULL(t3.total_annotated, 0) total_annotated FROM (SELECT DISTINCT mebsuta_api_cell_image.library_id FROM mebsuta_api_cell_image ORDER BY mebsuta_api_cell_image.library_id) t1 LEFT JOIN (SELECT mebsuta_api_debris.library_id, count(mebsuta_api_debris.id) as total_debris from mebsuta_api_debris WHERE mebsuta_api_debris.isDebris = true GROUP BY mebsuta_api_debris.library_id) t2 on t1.library_id = t2.library_id LEFT JOIN(SELECT mebsuta_api_annotation.library_id, count(DISTINCT(mebsuta_api_annotation.id)) as total_annotated from mebsuta_api_annotation GROUP BY mebsuta_api_annotation.library_id) t3 on t1.library_id = t3.library_id')
            data = dictfetchall(c)
            serializer = AnnotationDebrisRollUpSerializer(data, many=True)
            return Response(serializer.data)
