import unittest
import datetime

from unittest.mock import MagicMock, AsyncMock, Mock
from sqlalchemy.ext.asyncio import AsyncSession

from src.entity.models import Contact, User
from src.schemas.contact import ContactSchema, ContactUpdateSchema
from src.repository.contacts import (
    get_contacts,
    get_all_contacts,
    get_contact,
    create_contact,
    update_contact,
    delete_contact,
    search_contacts,
    get_upcoming_birthdays,
)


class TestAsyncContact(unittest.IsolatedAsyncioTestCase):

    def setUp(self) -> None:
        self.user = User(id=1, username="test_user", password="qwerty", confirmed=True, avatar="default_avatar.png")
        self.session = AsyncMock(spec=AsyncSession)

    async def test_get_all_contact(self):
        limit = 10
        offset = 0
        contacts = [
            Contact(
                id=1,
                first_name="test_first_name_1",
                last_name="test_last_name_1",
                email="test_email@example.com_1",
                phone="test_phone_1",
                birthday=datetime.date.today(),
                additional_info="test_additional_info_1",
                user=self.user,
            ),
            Contact(
                id=2,
                first_name="test_first_name_2",
                last_name="test_last_name_2",
                email="test_email@example.com_2",
                phone="test_phone_2",
                birthday=datetime.date.today(),
                additional_info="test_additional_info_2",
                user=self.user,
            ),
        ]
        mocked_contacts = MagicMock()
        mocked_contacts.scalars.return_value.all.return_value = contacts
        self.session.execute.return_value = mocked_contacts
        result = await get_all_contacts(limit, offset, self.session)
        self.assertEqual(result, contacts)

    async def test_get_contacts(self):
        limit = 10
        offset = 0
        contacts = [
            Contact(
                id=1,
                first_name="test_first_name_1",
                last_name="test_last_name_1",
                email="test_email@example.com_1",
                phone="test_phone_1",
                birthday=datetime.date.today(),
                additional_info="test_additional_info_1",
                user=self.user,
            ),
            Contact(
                id=2,
                first_name="test_first_name_2",
                last_name="test_last_name_2",
                email="test_email@example.com_2",
                phone="test_phone_2",
                birthday=datetime.date.today(),
                additional_info="test_additional_info_2",
                user=self.user,
            ),
        ]
        mocked_contacts = Mock()
        mocked_contacts.scalars.return_value.all.return_value = contacts
        self.session.execute.return_value = mocked_contacts
        result = await get_contacts(limit, offset, self.session, self.user)
        self.assertEqual(result, contacts)

    async def test_create_contact(self):
        body = ContactSchema(
            first_name="test_first_name",
            last_name="test_last_name",
            email="test_email@example.com",
            phone="test_phone",
            birthday=datetime.date.today(),
            additional_info="test_additional_info",
        )
        result = await create_contact(body, self.session, self.user)
        self.assertIsInstance(result, Contact)
        self.assertEqual(body.first_name, "test_first_name")
        self.assertEqual(body.last_name, "test_last_name")
        self.assertEqual(body.email, "test_email@example.com")
        self.assertEqual(body.phone, "test_phone")
        self.assertEqual(body.birthday, datetime.date.today())
        self.assertEqual(body.additional_info, "test_additional_info")

    async def test_update_contact(self):
        body = ContactUpdateSchema(
            first_name="test_first_name",
            last_name="test_last_name",
            email="test_email@example.com",
            phone="test_phone",
            birthday=datetime.date.today(),
            additional_info="test_additional_info",
            completed=True,
        )
        mocked_contact = MagicMock()
        mocked_contact.scalar_one_or_none.return_value = Contact(
            id=1,
            first_name="test_first_name",
            last_name="test_last_name",
            email="test_email@example.com",
            phone="test_phone",
            birthday=datetime.date.today(),
            additional_info="test_additional_info",
            user=self.user,
        )
        self.session.execute.return_value = mocked_contact
        result = await update_contact(1, body, self.session, self.user)
        self.assertIsInstance(result, Contact)
        self.assertEqual(body.first_name, "test_first_name")
        self.assertEqual(body.last_name, "test_last_name")
        self.assertEqual(body.email, "test_email@example.com")
        self.assertEqual(body.phone, "test_phone")
        self.assertEqual(body.birthday, datetime.date.today())
        self.assertEqual(body.additional_info, "test_additional_info")

    async def test_delete_contact(self):
        mocked_contact = MagicMock()
        mocked_contact.scalar_one_or_none.return_value = Contact(
            id=1,
            first_name="test_first_name",
            last_name="test_last_name",
            email="test_email@example.com",
            phone="test_phone",
            birthday=datetime.date.today(),
            additional_info="test_additional_info",
            user=self.user,
        )
        self.session.execute.return_value = mocked_contact
        result = await delete_contact(1, self.session, self.user)
        self.session.delete.assert_called_once()
        self.session.commit.assert_called_once()

        self.assertIsInstance(result, Contact)
