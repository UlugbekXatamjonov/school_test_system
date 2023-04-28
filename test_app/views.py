from django.shortcuts import render
from pprint import pprint
import json

from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework import viewsets, status
from rest_framework.response import Response

from .models import Sub_Category, Category, Question, Answer
from .serializer import Sub_CategoryAPISerializer, CategoryAPISerializer, QuestionAPISerializer, AnswerAPISerializer, ResultSerializer, \
    SelectSub_CategoryAPISerializer, SelectCategoryAPISerializer

from user_app.models import Result, Student

# Viewset for API serializers


class SelectCategoryViewset(viewsets.ModelViewSet):
    """
    ota-ona farzandi uchun category tanlab berishi uchun hamma kategorilar
    """
    queryset = Category.objects.filter(status="active")
    serializer_class = SelectCategoryAPISerializer
    lookup_field = 'slug'
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Category.objects.filter(status='active')


class SelectSub_CategoryViewset(viewsets.ModelViewSet):
    """
    ata-ona farzandi uchun subcategory tanlab berishi uchun hamma subcategorilar
    """
    queryset = Sub_Category.objects.filter(status="active")
    serializer_class = SelectSub_CategoryAPISerializer
    lookup_field = 'slug'
    permission_classes = [IsAuthenticated]


class CategoryViewset(viewsets.ModelViewSet):
    """
    Ota-ona tanlaganda bolaga ko'rinadigan categorilar
    """
    queryset = Category.objects.filter(status="active")
    serializer_class = CategoryAPISerializer
    lookup_field = 'slug'
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            try:
                subcategory = Sub_Category.objects.filter(
                    id=user.student_tests.id).values()
                return Category.objects.filter(id=subcategory[0]['parent_id'])
            except Exception:
                return Category.objects.none()
        return Category.objects.none()


class Sub_CategoryViewset(viewsets.ModelViewSet):
    """
    Ota-ona tanlaganda bolaga ko'rinadigan subcategorilar
    """
    queryset = Sub_Category.objects.filter(status="active")
    serializer_class = Sub_CategoryAPISerializer
    lookup_field = 'slug'
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            # print('*********************************')
            # print(user.student_tests.id)
            # print('*********************************')

            return Sub_Category.objects.filter(id=user.student_tests.id)
        return Sub_Category.objects.none()


class QuestionViewset(viewsets.ModelViewSet):
    queryset = Question.objects.filter(status="active")
    serializer_class = QuestionAPISerializer
    lookup_field = 'slug'
    permission_classes = [IsAuthenticated]


class AnswerViewset(viewsets.ModelViewSet):
    queryset = Answer.objects.filter(status="active")
    serializer_class = AnswerAPISerializer
    lookup_field = 'slug'
    permission_classes = [IsAuthenticated]


""" ------------------------ CRUD Viewset -------------------- """


class ResultViewset(viewsets.ModelViewSet):
    """
    O'quvchi test yechganda, yechilgan testni balini berilgan bir nechta parametrlar
    bo'yicha hisoblab chiqadi.
    To'plangan balga qarab belgilangan 'teashxis' yani hulosa olinadi
    """
    queryset = Result.objects.all()
    serializer_class = ResultSerializer
    permission_classes = [AllowAny]

    """ CRUD operations """

    def create(self, request, *args, **kwargs):
        result_data = request.data

        """
        ----------------------------- CALCULATE BALL'S AND RETURN RESULT  ---------------------
        Requestdan keloyatgan malumotlar asosida foydalanuvchi ishlagan test natijalariga ko'ra ballar 
            hisoblab chiqiladi va ballga mos hulosa chiqariladi.
        --------------------------------------   START   ---------------------------------------
        """

        """ ------------------------- Xatolik turlari --------------------------------- 
            101 - Requestdan kelgan malumotlarni ajratib olishda sodir bo'ladi
            102 - Requestdan kelgan malumotlar asosida bazadagi mos malumotlarni ajratib olishda sodir bo'ladi
            103 - Testning ball hisoblash qismida xatolik yuz berdi
        """

        """ Requestdan kelgan malumotlar ajratib olinadi(o'zining asl ma'lumot turida) """
        try:
            # requestdan kelgan category id si
            request_category = int(result_data['category'])
            # requestdan kelgan subcategory id si
            request_subcategory = int(result_data['subcategory'])

            # requestdan kelgan testlar va belgilangan javoblar json dan asl ma'lumot turiga o'tgazildi
            request_tests = json.loads(result_data['test_api'])
            # faqat 'test_id' va 'answer_id' bo'limi ajratib olindi
            request_tests = request_tests['tests']
            request_test_ids = []  # requestdan kelgan testlar idsi to'plangan list
            request_answer_ids = []  # requestdan kelgan answer idsi to'plangan list
            for test in request_tests:  # tsikl yordamida test va answer idlarini bo'sh ro'yhatga qo'shib olindi
                request_test_ids.append(test['test_id'])
                request_answer_ids.append(test['answer_id'])
        except:
            return Response({'error': "101 - xatolik turi aniqlandi(ResultViewset)"})

        """ Requestdan kelgan malumotlar asosida bazadagi mos malumotlarni ajratib olamiz """
        try:
            data_category = Category.objects.filter(
                id=request_category).values()
            data_subcategory = Sub_Category.objects.filter(
                id=request_subcategory).values()
            # bazadan ajratib olingan ma'lumotlar 'list' bo'lagni uchun uni 'index'si bn olib olindi
            data_category = data_category[0]
            # bazadan ajratib olingan ma'lumotlar 'list' bo'lagni uchun uni 'index'si bn olib olindi
            data_subcategory = data_subcategory[0]

            data_tests = []  # bazadan ajratib olingan 'test'lar(obyektlar)
            for test_id in request_test_ids:  # requestdan kelgan test 'id'lari asosida shu 'id'ga mos bazadagi testlar obyekt ko'rinishida ro'yhatga yig'ib olindi
                t = Question.objects.filter(id=test_id).values()
                # bazadan ajratib olingan 't' list bo'lgani uchun 0-'index'dagi qiymat olinyapdi
                data_tests.append(t[0])

            data_answers = []  # bazadan ajratib olingan 'answer'lar(obyektlar)
            for answer_id in request_answer_ids:  # requestdan kelgan 'answer' 'id'lari asosida shu 'id'ga mos bazadagi 'answer'lar obyekt ko'rinishida ro'yhatga yig'ib olindi
                a = Answer.objects.filter(id=answer_id).values()
                # bazadan ajratib olingan 'a' list bo'lgani uchun 0-'index'dagi qiymat olinyapdi
                data_answers.append(a[0])
        except:
            return Response({'error': "102 - xatolik turi aniqlandi(ResultViewset)"})

        """ Bazadan tanlab olingan 'test'lar asosida ularning 'ballar'ini kerakli parametrlarga asoslanib
                ajratib olinadi va 'ball'ga mos bo'lgan 'hulosa' aniqlanadi 
        """
        try:
            total_ball = 0  # O'quvchi tomonidan belgilangan javoblar ostidagi ballar yig'indisi
            # O'quvchi tomonidan belgilangan javoblardan yig'ilgan ummumiy 'ball'ga ko'ra belgilangan 'hulosa'
            total_hulosa = "Hulosa mavjud emas!"

            """ <Emotsional holati va stressni aniqlash> testlar turi uchun ummumiy 'ball' va 'hulosani' aniqlash """
            if data_subcategory['question_type'] == 'ehsa':  # Emotsional holati va stressni aniqlash
                for answer in data_answers:
                    total_ball += answer['ball']

                if total_ball < 40:
                    total_hulosa = "Siz bazan past stress holatiga tushib qolasiz. Lekin shunda ham o'zingizni boshqara olasiz"
                elif total_ball >= 40 and total_ball < 48:
                    total_hulosa = "Vaqti-vaqti bilan stress holatiga tushib qolasiz. Siz o'rtacha stress holatidasiz"
                elif total_ball >= 48:
                    total_hulosa = "Hayot tarzingizni qayta ko'rib chiqing. Sizda yuqori darajadgi stress kuzatilmoqda. \
                    Stressdan chiqish uchun psixolog konsultatntga murojat qiling"
                else:  # ehtiyot uchun
                    total_hulosa = "Hulosani aniqlashda dastur xatoligi !"

            """ <O'quvchi tepmeramentini aniqlash> testlar turi uchun ummumiy 'ball' va 'hulosani' aniqlash """
            if data_subcategory['question_type'] == 'ota':  # <O'quvchi tepmeramentini aniqlash>
                total_ball = 0
                # Belgilangan yagona javob asosida, shu javob ostidagi 'question_result' olinadi va hulosaga uzatiladi
                total_hulosa = data_answers[0]['question_result']

            """ <KASB TANLASHGA TAYYORLIKNI ANIQLASH> testlar turi uchun ummumiy 'ball' va 'hulosani' aniqlash """
            if data_subcategory['question_type'] == 'ktta':  # <KASB TANLASHGA TAYYORLIKNI ANIQLASH>
                for answer_c in data_answers:
                    total_ball += answer_c['ball']

                if total_ball >= 0 and total_ball <= 2:
                    total_hulosa = "Siz uchun kasb tanlash muammosi allaqachon hal bo'lgan. Bizning kasblar dunyosidan xabardorlik darajangiz va uni qanday tanlashingiz yaxshi mutaxassis maqomiga deyarli teng"
                elif total_ball >= 3 and total_ball <= 5:
                    total_hulosa = "Siz hali kasb qanday tanlanishi haqida yetarli ma'lumotga ega emassiz. Ehtimol, yordam so'rash vaqti kelgandir"
                elif total_ball >= 6 and total_ball <= 10:
                    total_hulosa = "Siz ko'plab fikrlarga qo'shildingiz, endi bu savolga chin dildan javob berishga harakat qiling: 'Nega javobgarlikni o'z zimmamga olishim qiyin?' Balki bu savolga javob berib qanday qilib mustaqil fikrga ega bo'lishni anglab yetarsiz"
                else:
                    total_hulosa = "Hulosani aniqlashda dastur xatoligi !"

            """ <Kasb tiplarini aniqlash> testlar turi uchun ummumiy 'ball' va 'hulosani' aniqlash """
            if data_subcategory['question_type'] == 'kta':  # <Kasb tiplarini aniqlash>
                for answer_c in data_answers:
                    total_ball += answer_c['ball']

                job_balls = {
                    'tabiat': 0,
                    "texnika": 0,
                    "belgi": 0,
                    "sanat": 0,
                    "inson": 0,
                }

                job_hulosa = {
                    'tabiat': "Bilolog, Zoolog, Zootexnik, agranom,gidrolog, geology, qishloq xo’jaligi mutaxxasisi kabi tabiat va  atrof muhit bilan bog’liq kasblarga layoqi baland",
                    "texnika": "Elektik, Avtomobilsozlik bo’yicha mutaxasis, kompyuter injinering, Santexnik kabi kasblarga layoqati baland",
                    "belgi": "Dasturchilar, Kotib, Bank xodimi, Bugalter, Moliya soxasi mutaxasisi, statistic kabi kasblarga layoqati baland",
                    "sanat": "Xaykaltaroshlik, Rassomlik, Aktyorlik, Sozandalik, Xonandalik, Bastakor, derijor, raqqosa kabi kasblarga layoqati baland",
                    "inson": "O’qituvchi , shifokor, tarbiyachi, huquqshunos, ichki ishlar xodimi, savdogar kabi odamlar bilan ko’p muloqot qiladigan kasblarga layoqati baland",
                }

                for test_couple in request_tests:
                    """ Belgilangan variantlardan kasb bo'yicha to'plangan ballni hisoblash """
                    data_test = Question.objects.filter(
                        id=test_couple['test_id']).values().first()
                    data_answer = Answer.objects.filter(
                        id=test_couple['answer_id']).values().first()

                    if data_test['job_type'] == 'tabiat' and data_answer['ball'] == 1:
                        job_balls['tabiat'] += data_answer['ball']
                    elif data_test['job_type'] == 'texnika' and data_answer['ball'] == 1:
                        job_balls['texnika'] += data_answer['ball']
                    elif data_test['job_type'] == 'belgi' and data_answer['ball'] == 1:
                        job_balls['belgi'] += data_answer['ball']
                    elif data_test['job_type'] == 'sanat' and data_answer['ball'] == 1:
                        job_balls['sanat'] += data_answer['ball']
                    elif data_test['job_type'] == 'inson' and data_answer['ball'] == 1:
                        job_balls['inson'] += data_answer['ball']
                    else:
                        continue

                job_keys = []  # bali eng yuqori  bo'lgan kasblar ro'yhati --> key
                result = {}  # bali eng yuqori  bo'lgan kasblar lug'ati --> key-vaue
                # 'job_balls' lug'atidan eng yuqori valuesi bor qiymatlarni ajratib olamiz
                max_value = max(job_balls.values())
                for k, v in job_balls.items():
                    if v == max_value:
                        job_keys.append(k)
                        result[k] = v

                total_hulosa = ''
                for key, value in job_hulosa.items():
                    if key in job_keys:
                        total_hulosa += f"{value}\n\n"
        except:
            return Response({'error': "103 - xatolik turi aniqlandi(ResultViewset)"})

        """
        ----------------------------- CALCULATE BALL'S AND RETURN RESULT  ---------------------
        ---------------------------------------  FINISH   -------------------------------------
        """

        user = False
        if 'user' in result_data:
            try:
                if int(result_data['user']) == int(request.user.id):
                    user = Student.objects.get(pk=str(result_data['user']))
                else:
                    return Response({"error": "Ro'yhatdan o'tgan user 'id'si, test yechgan user 'id'siga to'g'ri kelmadi!!!"})

            except Exception as e:
                return Response({"error": "Bunday user mavjud emas!!!"})

        category = False
        if 'category' in result_data:
            try:
                category = Category.objects.get(
                    pk=str(result_data['category']))
            except Exception as e:
                return Response({"error": "Bunday kategoriya mavjud emas!!!"})

        subcategory = False
        if 'subcategory' in result_data:
            try:
                subcategory = Sub_Category.objects.get(
                    pk=str(result_data['subcategory']))
            except Exception as e:
                return Response({"error": "Bunday kichik kategoriya mavjud emas!!!"})

        try:
            new_result = Result.objects.create(
                user=user,
                category=category,
                subcategory=subcategory,
                ball=total_ball,
                tashxis=total_hulosa,
                test_api={'api': "API"}
            )
            new_result.save()
            serializer = ResultSerializer(new_result)
            return Response(serializer.data)
        except Exception as e:
            return Response({'errors': "Ma'lumot to'liq emas!!!"})
