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
        self.state = kwargs.get('state')

        if kwargs.get('description') is not None:
            self.description = DescriptionConfig(**kwargs.get('description'))
        self.labels = kwargs.get('labels')

        if kwargs.get('date') is not None:
            self.date = DateConfig(**kwargs.get('date'))


@dataclass()
class LabelConfig:
    remove: list[str]

    def __init__(self, **kwargs):
        self.remove = kwargs.get('remove')


@dataclass()
class IssueConfigParser:
    comment: str
    conditions: ConditionConfig = None
    labels: LabelConfig = None

    def __init__(self, **kwargs):
        self.comment = kwargs.get('comment')
        if kwargs.get('conditions') is not None:
            self.conditions = ConditionConfig(**kwargs.get('conditions'))
        if kwargs.get('labels') is not None:
            self.labels = LabelConfig(**kwargs.get('labels'))

    def parse(self, issue):
        self.comment = self.comment.replace(
            '{{author}}', issue.author['username'])
        if self._description_condition(issue.description) == False:
            return False
        if self._labels_condition(issue.labels) == False:
            return False
        if self._date_condition(issue) == False:
            return False
        self._labels(issue)
        return True

    def _labels(self, issue):
        if self.labels is None:
            return True
        if self.labels.remove:
            for i, label in enumerate(issue.labels):
                if (len(issue.labels) <= 0):
                    break
                for old_label in self.labels.remove:
                    if old_label in label:
                        if (len(issue.labels) <= 0):
                            break
                        issue.labels.pop(i)
        issue.save()

        pass

    def _date_condition(self, attr):
        if self.conditions.date is None:
            return True
        x = datetime.datetime.fromisoformat(
            attr.updated_at.replace('Z', ''))
        interval_type = self.conditions.date.interval_type
        interval = self.conditions.date.interval
        now = datetime.datetime.now()
        delta = now - datetime.timedelta(**{interval_type: interval})
        if self.conditions.date.condition == 'older_than':
            if x < delta:
                return True
        else:
            if x > delta:
                return True
        return False

    def _description_condition(self, attr: str):
        if self.conditions.description is None:
            return True
        if attr is not None and len(attr) < self.conditions.description.length:
            return True
        return False

    def _labels_condition(self, attr: list[str]):
        if self.conditions.labels is None:
            return True
        if self.conditions.labels.get('must') is None:
            return True

        text = ''
        for label in self.conditions.labels['must']:
            if any(label in s for s in attr):
                continue
            text += f'`{label}` '
        if text.strip() == '':
            return False
        else:
            self.comment = self.comment.replace(
                '{{labels}}', text.strip().replace(' ', ','))
            return True
