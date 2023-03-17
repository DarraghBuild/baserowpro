from .airtable import AirtableFixtures
from .application import ApplicationFixtures
from .auth_provider import AuthProviderFixtures
from .element import ElementFixtures
from .field import FieldFixtures
from .file_import import FileImportFixtures
from .job import JobFixtures
from .page import PageFixtures
from .row import RowFixture
from .settings import SettingsFixtures
from .snapshots import SnapshotFixtures
from .table import TableFixtures
from .template import TemplateFixtures
from .token import TokenFixtures
from .user import UserFixtures
from .user_file import UserFileFixtures
from .view import ViewFixtures
from .webhook import TableWebhookFixture
from .workspace import WorkspaceFixtures


class Fixtures(
    SettingsFixtures,
    UserFixtures,
    UserFileFixtures,
    WorkspaceFixtures,
    ApplicationFixtures,
    TableFixtures,
    ViewFixtures,
    FieldFixtures,
    TokenFixtures,
    TemplateFixtures,
    RowFixture,
    TableWebhookFixture,
    AirtableFixtures,
    JobFixtures,
    FileImportFixtures,
    SnapshotFixtures,
    AuthProviderFixtures,
    PageFixtures,
    ElementFixtures,
):
    def __init__(self, fake=None):
        self.fake = fake
