"""공통 예외 정의."""


class MigrationNotAppliedError(Exception):
    """마이그레이션이 적용되지 않은 상태에서 DB 접근 시 발생."""
