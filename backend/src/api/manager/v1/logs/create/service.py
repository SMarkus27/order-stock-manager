from sqlalchemy.ext.asyncio import AsyncSession

from src.models.entities.logs import AuditLog


class AuditLogService:
    @staticmethod
    async def log(
        session: AsyncSession,
        entity: str,
        action: str,
        entity_id: str,
        message: str,
    ):
        log = AuditLog(
            entity=entity,
            action=action,
            entity_id=str(entity_id),
            message=message,
        )

        session.add(log)
