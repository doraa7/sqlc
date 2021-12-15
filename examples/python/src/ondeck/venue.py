# Code generated by sqlc. DO NOT EDIT.
import dataclasses
from typing import AsyncIterator, List, Optional

import sqlalchemy
import sqlalchemy.ext.asyncio

from ondeck import models



CREATE_VENUE = """-- name: create_venue \\:one
INSERT INTO venue (
    slug,
    name,
    city,
    created_at,
    spotify_playlist,
    status,
    statuses,
    tags
) VALUES (
    :p1,
    :p2,
    :p3,
    NOW(),
    :p4,
    :p5,
    :p6,
    :p7
) RETURNING id
"""


@dataclasses.dataclass()
class CreateVenueParams:
    slug: str
    name: str
    city: str
    spotify_playlist: str
    status: models.Status
    statuses: Optional[List[models.Status]]
    tags: Optional[List[str]]


DELETE_VENUE = """-- name: delete_venue \\:exec
DELETE FROM venue
WHERE slug = :p1 AND slug = :p1
"""


GET_VENUE = """-- name: get_venue \\:one
SELECT id, status, statuses, slug, name, city, spotify_playlist, songkick_id, tags, created_at
FROM venue
WHERE slug = :p1 AND city = :p2
"""


LIST_VENUES = """-- name: list_venues \\:many
SELECT id, status, statuses, slug, name, city, spotify_playlist, songkick_id, tags, created_at
FROM venue
WHERE city = :p1
ORDER BY name
"""


UPDATE_VENUE_NAME = """-- name: update_venue_name \\:one
UPDATE venue
SET name = :p2
WHERE slug = :p1
RETURNING id
"""


VENUE_COUNT_BY_CITY = """-- name: venue_count_by_city \\:many
SELECT
    city,
    count(*)
FROM venue
GROUP BY 1
ORDER BY 1
"""


@dataclasses.dataclass()
class VenueCountByCityRow:
    city: str
    count: int


class AsyncQuerier:
    def __init__(self, conn: sqlalchemy.ext.asyncio.AsyncConnection):
        self._conn = conn

    async def create_venue(self, arg: CreateVenueParams) -> Optional[int]:
        row = (await self._conn.execute(sqlalchemy.text(CREATE_VENUE), {
            "p1": arg.slug,
            "p2": arg.name,
            "p3": arg.city,
            "p4": arg.spotify_playlist,
            "p5": arg.status,
            "p6": arg.statuses,
            "p7": arg.tags,
        })).first()
        if row is None:
            return None
        return row[0]

    async def delete_venue(self, *, slug: str) -> None:
        await self._conn.execute(sqlalchemy.text(DELETE_VENUE), {"p1": slug})

    async def get_venue(self, *, slug: str, city: str) -> Optional[models.Venue]:
        row = (await self._conn.execute(sqlalchemy.text(GET_VENUE), {"p1": slug, "p2": city})).first()
        if row is None:
            return None
        return models.Venue(
            id=row[0],
            status=row[1],
            statuses=row[2],
            slug=row[3],
            name=row[4],
            city=row[5],
            spotify_playlist=row[6],
            songkick_id=row[7],
            tags=row[8],
            created_at=row[9],
        )

    async def list_venues(self, *, city: str) -> AsyncIterator[models.Venue]:
        result = await self._conn.stream(sqlalchemy.text(LIST_VENUES), {"p1": city})
        async for row in result:
            yield models.Venue(
                id=row[0],
                status=row[1],
                statuses=row[2],
                slug=row[3],
                name=row[4],
                city=row[5],
                spotify_playlist=row[6],
                songkick_id=row[7],
                tags=row[8],
                created_at=row[9],
            )

    async def update_venue_name(self, *, slug: str, name: str) -> Optional[int]:
        row = (await self._conn.execute(sqlalchemy.text(UPDATE_VENUE_NAME), {"p1": slug, "p2": name})).first()
        if row is None:
            return None
        return row[0]

    async def venue_count_by_city(self) -> AsyncIterator[VenueCountByCityRow]:
        result = await self._conn.stream(sqlalchemy.text(VENUE_COUNT_BY_CITY))
        async for row in result:
            yield VenueCountByCityRow(
                city=row[0],
                count=row[1],
            )
