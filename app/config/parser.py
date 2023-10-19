from typing_extensions import Literal
from dataclasses import dataclass
import datetime


@dataclass()
class DateConfig:
    attribute: str
    condition: str
    interval_type: Literal['days', 'weeks', 'months']
    interval: int

    def __init__(self, **kwargs):
        self.attribute = kwargs.get('attribute')
        self.condition = kwargs.get('condition')
        self.interval_type = kwargs.get('interval_type')
        self.interval = kwargs.get('interval')


@dataclass()
class DescriptionConfig:
    length: int

    def __init__(self, **kwargs):
        self.length = kwargs.get('length')


@dataclass()
class ConditionConfig:
    state: str
    labels: str
    description: DescriptionConfig = None
    date: DateConfig = None

    def __init__(self, **kwargs):
        print(kwargs.get('name'))
        self.state = kwargs.get('state')

        if kwargs.get('description') is not None:
            self.description = DescriptionConfig(**kwargs.get('description'))
        self.labels = kwargs.get('labels')

        if kwargs.get('date') is not None:
            self.date = DateConfig(**kwargs.get('date'))


@dataclass()
class Parser:
    comment: str
    conditions: ConditionConfig = None

    def __init__(self, **kwargs):
        self.comment = kwargs.get('comment')
        if kwargs.get('conditions') is not None:
            self.conditions = ConditionConfig(**kwargs.get('conditions'))

    def date(self, attr):
        x = datetime.datetime.fromisoformat(
            attr['updated_at'].replace('Z', ''))
        interval_type = self.conditions.date.interval_type
        interval = self.conditions.date.interval
        now = datetime.datetime.now()
        delta = now - datetime.timedelta(**{interval_type: interval})
        if self.date['condition'] == 'older_than':
            if x < delta:
                return True
        else:
            if x > delta:
                return True
        return False

    def description(self, attr: str):
        if attr is not None and len(attr) < self.conditions.description.length:
            return True
        return False

    # def labels(self, attr: list[str]):
    #     if self.labels.get('must') is not None:
    #         text = ''
    #         for label in self.labels['must']:
    #             if any(label in s for s in attr):
    #                 continue
    #             text += f'`{label}` '
    #         if text.strip() == '':
    #             return False
    #         else:
    #             self.comment = self.comment.replace(
    #                 '{{labels}}', text.strip().replace(' ', ','))
    #             return True
    #     return False
