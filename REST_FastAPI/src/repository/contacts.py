from fastapi import HTTPException
from sqlalchemy import select, or_, and_
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta, date

from src.entity.models import Contact, User
from src.schemas.contact import ContactSchema, ContactUpdateSchema
import logging


async def get_contacts(limit: int, offset: int, db: AsyncSession, user: User):
    """
    The get_contacts function returns a list of contacts for the user.

    :param limit: int: Limit the number of contacts returned.
    :param offset: int: Skip the first n results.
    :param db: AsyncSession: Pass a database connection to the function.
    :param user: User: Filter the contacts by user.
    :return: A list of contacts objects.
    """
    stmt = select(Contact).filter_by(user=user).offset(offset).limit(limit)
    contacts = await db.execute(stmt)
    return contacts.scalars().all()


async def get_all_contacts(limit: int, offset: int, db: AsyncSession):
    """
    The get_all_contacts function returns a list of all contacts in the database.

    :param limit: int: Limit the number of contacts returned.
    :param offset: int: Specify how many rows to skip.
    :param db: AsyncSession: Pass the database connection to the function.
    :return: A list of contacts objects.
    """
    stmt = select(Contact).offset(offset).limit(limit)
    contacts = await db.execute(stmt)
    return contacts.scalars().all()


async def get_contact(contact_id: int, db: AsyncSession, user: User):
    """
    The get_contact function takes in an id, and returns the contact object with that id.

    :param contact_id: int: Specify the id of the contact to get.
    :param db: AsyncSession: Pass the database session to the function.
    :param user: User: Get the user who created the contact.
    :return: A contact object.
    """
    stmt = select(Contact).filter_by(id=contact_id, user=user)
    contact = await db.execute(stmt)
    return contact.scalar_one_or_none()


async def create_contact(body: ContactSchema, db: AsyncSession, user: User):
    """
    Creates a new contact for a specific user.

    :param body: The data for the contact to create.
    :param user: The user to create the contact for.
    :param db: AsyncSession: Pass the database session to the function.
    :return: The newly created contact.
    """
    contact = Contact(
        **body.model_dump(exclude_unset=True), user=user
    )  # (name=body.name, etc.)
    db.add(contact)
    await db.commit()
    await db.refresh(contact)
    return contact


async def update_contact(
    contact_id: int, body: ContactUpdateSchema, db: AsyncSession, user: User
):
    """
    Updates a single contact with the specified ID for a specific user.

    :param contact_id: The ID of the contact to update.
    :param body: The updated data for the contact.
    :param user: The user to update the contact for.
    :param db: AsyncSession: Pass the database session to the function.
    :return: The updated contact.
    """
    stmt = select(Contact).filter_by(id=contact_id, user=user)
    result = await db.execute(stmt)
    contact = result.scalar_one_or_none()
    if contact:
        contact.first_name = body.first_name
        contact.last_name = body.last_name
        contact.email = body.email
        contact.phone = body.phone
        contact.birthday = body.birthday
        contact.additional_info = body.additional_info
        contact.completed = body.completed
        await db.commit()
        await db.refresh(contact)
    return contact


async def delete_contact(contact_id: int, db: AsyncSession, user: User):
    """
    Removes a single contact with the specified ID for a specific user.

    :param contact_id: The ID of the contact to remove.
    :param user: The user to remove the contact for.
    :param db: AsyncSession: Pass the database session to the function.
    :return: The removed contact.
    """
    stmt = select(Contact).filter_by(id=contact_id, user=user)
    contact = await db.execute(stmt)
    contact = contact.scalar_one_or_none()
    if contact:
        await db.delete(contact)
        await db.commit()
    return contact


async def search_contacts(query: str, db: AsyncSession):
    """
    Searches for contacts in the database that match a given query string in their first name, last name, or email.

    :param query: The search string to look for in the contacts' first name, last name, or email.
    :param db: AsyncSession: Pass the database session to the function.
    :return: A list of contacts that match the search query.
    """
    stmt = select(Contact).filter(
        or_(
            Contact.first_name.ilike(f"%{query}%"),
            Contact.last_name.ilike(f"%{query}%"),
            Contact.email.ilike(f"%{query}%"),
        )
    )
    contacts = await db.execute(stmt)
    return contacts.scalars().all()


async def get_upcoming_birthdays(db: AsyncSession):
    """
    Retrieves a list of contacts with upcoming birthdays within the next 7 days, adjusting the birthday celebration date if it falls on a weekend.

    :param db: AsyncSession: Pass the database session to the function.
    :return: A list of dictionaries with contact names and their adjusted birthday celebration dates within the next 7 days.
    """
    try:
        today = date.today()
        upcoming_birthdays = []
        stmt = select(Contact)
        result = await db.execute(stmt)
        records = result.scalars().all()

        for record in records:
            birthday = record.birthday
            birthday_this_year = birthday.replace(year=today.year)

            if birthday_this_year < today:
                birthday_this_year = birthday_this_year.replace(year=today.year + 1)

            days_until_birthday = (birthday_this_year - today).days

            if days_until_birthday <= 7:
                if birthday_this_year.weekday() == 5:
                    birthday_this_year += timedelta(days=2)
                elif birthday_this_year.weekday() == 6:
                    birthday_this_year += timedelta(days=1)

                upcoming_birthdays.append(
                    {
                        "name": f"{record.first_name} {record.last_name}",
                        "congratulation_date": birthday_this_year.strftime("%d.%m.%Y"),
                    }
                )

        return upcoming_birthdays
    except Exception as e:
        logging.error(f"Error fetching upcoming birthdays: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
