# -*- coding: utf-8 -*-

from helper import Religious, Prayer

hrist = Religious(
                'Христианство',
                ['Господу Богу твоему поклоняйся и Ему одному служи', 'Люби Бога своего и всех людей'],
                ['CAADAgADOAADGXMNCSqaRY-FOG6VAg'],
                {
                    'Отче наш': Prayer('AwADAgADVwADW5rZSvekof0PkgZBAg') ,
                    'Песнь Богородицы': Prayer('AwADAgADVQADW5rZSjicBmlpyILRAg'),
                    'Символ веры': Prayer('AwADAgADWAADW5rZSj2pan7ZxRsmAg'),
                    'Молитва кресту': Prayer('AwADAgADVgADW5rZSryvl4hANtGxAg'),
                })

buddizm = Religious(
                'Буддизм',
                ['Гармония приходит изнутри. Не ищите ее снаружи'],
                ['CAADAwADfAADyzaRAAFVPCGbs0CdwAI'])

gods = {
    'иисус': hrist,
    'иисус христос': hrist,
    'аллах': Religious(
                'Ислам',
                ['Нет никакого божества, кроме Аллаха, и Мухаммад — посланник Аллаха!'],
                 ['CAADBQADogAD_uTOAi1OxoF_OJCSAg']),
    'будда': buddizm,
    'будда шакьямуни': buddizm,
    'яхва': Religious(''),
    'бог яхва': Religious(''),
    'конфуций': Religious(''),
    'аматэрасу': Religious(''),
    'заратустра': Religious(''),
    'ахурамазда': Religious(''),
    'ариман': Religious(''),
    'путин': Religious(
                'Путианство',
                ['Я слежу за тобой, мой друг'])
}

phrases = [
    'Да прибудет с тобой сила!',
    'Все твои молитвы будут услышаны',
    'Если твоей душе это будет угодно, ты обязательно это обретешь'
]

plz_registrate = 'Пожалуйста, установите контакт с Богом'
cancel = 'Отмена'

offertory_message = """\
Да придет к тебе спасение Божье через отречение от земных благ, во имя бесконечного процветания. \
Нельзя почувствовать в себе Бога без очищения от изысков, нельзя понять веру. \
Только чистый дух - Cвят.
"""


help_message = """\
Вы можете просто общаться с Богом на любые темы, задавать вопросы, что-то просить или воспользоваться следующими командами:

/start - Заново установить контакт с Богом

/prayerbook - Молитвенник

/pray - Помолиться за раба Божьего

/offertory - Сделать пожертвование
/help - Помощь
"""
