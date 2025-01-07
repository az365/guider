from templates.knowledge.term import LinkedTerm


discipline = LinkedTerm(
    'discipline',
    synonymes=['дисциплина', 'наука', 'профессия'],
)
method = LinkedTerm(
    'method',
    synonymes=['method', 'метод'],
    definition='способ достижения какого-либо результата в некоторой области',
    uses=discipline,
)

da = LinkedTerm(
    'da',
    synonymes=['data analysis', 'анализ данных'],
    definition='построение выводов и рекомендаций на основе измеримых фактов, наблюдённых в данных',
    cls=discipline,
)
da_task_type = LinkedTerm(
    'da_task_type',
    synonymes=['DA-task(s)', 'DA-task type(s)', 'DA-задача(-и)', 'класс DA-задач', 'категория DA-задач'],
    definition='класс(ы) задач, решаемых в анализе данных',
    container=da,
)
da_method = LinkedTerm(
    'da_method',
    synonymes=['DA-method(s)', 'DA-метод(ы)', 'аналитический(-ие) метод(ы)'],
    definition='способ решения задач анализе данных',
    parent=method,
    container=da,
    usage=da_task_type,
)

pilot_eval_task = LinkedTerm(
    'pilot_eval_task',
    synonymes=['задача оценки эффекта воздействия'],
    definition='тип задач анализа данных, целью которого является оценка воздействия (пилота, события) на некоторую систему (аудитория, рынок, бизнес-процесс) по её метрикам',
    cls=da_task_type,
)
pilot_eval_methods = LinkedTerm(
    'pilot_eval_methods',
    synonymes=['методы оцени воздействия'],
    usage=pilot_eval_task,
)

managed_pilot_eval_task = LinkedTerm(
    'managed_pilot_eval_task',
    synonymes=['контролируемый эксперимент', 'задача оценки контролируемого эксперимента'],
    parent=pilot_eval_task,
)
retro_pilot_eval_task = LinkedTerm(
    'retro_pilot_eval_task',
    synonymes=['ретроспективный эксперимент', 'ретроспективная оценка воздействия', 'задача ретроспективной оценки воздействия'],
    parent=pilot_eval_task,
)
observational_study = LinkedTerm(
    'observational_study',
    synonymes=['observational study(-ies)', 'обсервационные исследования', 'оценка неконтролируемых воздействий'],
    parent=pilot_eval_task,
)

ci = LinkedTerm(
    'ci',
    synonymes=['CI', 'causal inference', 'причинно-следственный вывод', 'причинно-следственный анализ'],
    definition='методы исследования причинно-следственных связей',
    cls=da_method,
    usage=pilot_eval_task,
)
abt = LinkedTerm(
    'abt',
    synonymes=['ABT', 'АБТ', 'АБ-тестинг', 'AB-Testing'],
    definition='способ оценки внедрений через сравнение тестовой и контрольной выборок в контролируемом эксперимента',
    cls=da_method,
    container=ci,
    usage=managed_pilot_eval_task,
)
ps_methods = LinkedTerm(
    'ps_methods',
    synonymes=['PS', 'PS*', 'PS-methods', 'propensity score methods'],
    definition='методы оценки влияния воздействия, использующие оценки вероятностей объектов испытать воздействие',
    cls=da_method,
    container=ci,
    usage=[retro_pilot_eval_task, observational_study]
)
psm = LinkedTerm(
    'psm',
    synonymes=['PSM', 'propensity score matching'],
    definition='сравнение пар объектов, в которых один испытал некоторое воздействие, второй же имел схожую вероятность испытать воздействие, но не испытал',
    cls=da_method,
    container=ps_methods,
)
