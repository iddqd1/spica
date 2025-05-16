from typing import TYPE_CHECKING

import pytest

from spica.conftest import *  # noqa: F403

from . import factories

if TYPE_CHECKING:
    from survey import models


@pytest.fixture
def surveys(db) -> list["models.Survey"]:
    return factories.SurveyFactory.create_batch(5)
