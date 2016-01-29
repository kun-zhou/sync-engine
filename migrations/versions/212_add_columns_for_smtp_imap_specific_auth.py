"""Add columns for smtp/imap-specific auth

Revision ID: 501f6b2fef28
Revises: 31aae1ecb374
Create Date: 2016-01-29 00:27:08.174534

"""

# revision identifiers, used by Alembic.
revision = '501f6b2fef28'
down_revision = '31aae1ecb374'

from alembic import op
from sqlalchemy.sql import text


def upgrade():
    conn = op.get_bind()
    conn.execute(text("set @@lock_wait_timeout = 20;"))
    conn.execute(text("SET FOREIGN_KEY_CHECKS=0;"))
    # Add new columns.
    conn.execute(text("ALTER TABLE genericaccount ADD COLUMN imap_username CHAR(255) DEFAULT NULL"))
    conn.execute(text("ALTER TABLE genericaccount ADD COLUMN smtp_username CHAR(255) DEFAULT NULL"))
    conn.execute(text("ALTER TABLE genericaccount ADD COLUMN imap_password_id BIGINT(20)"))
    conn.execute(text("ALTER TABLE genericaccount ADD COLUMN smtp_password_id BIGINT(20)"))
    # Add ForeignKey constraints.
    conn.execute(text("ALTER TABLE genericaccount ADD CONSTRAINT imap_password_id_ifbk FOREIGN KEY "
                      "(`imap_password_id`) REFERENCES `secret` (`id`)"))
    conn.execute(text("ALTER TABLE genericaccount ADD CONSTRAINT smtp_password_id_ifbk FOREIGN KEY "
                      "(`smtp_password_id`) REFERENCES `secret` (`id`)"))
    # Copy appropriate table values.
    conn.execute(text("UPDATE genericaccount SET genericaccount.imap_username = (SELECT account._raw_address "
                      "FROM account WHERE genericaccount.id = account.id)"))
    conn.execute(text("UPDATE genericaccount SET genericaccount.smtp_username = (SELECT account._raw_address "
                      "FROM account WHERE genericaccount.id = account.id)"))
    conn.execute(text("UPDATE genericaccount SET imap_password_id = password_id"))
    conn.execute(text("UPDATE genericaccount SET smtp_password_id = password_id"))


def downgrade():
    conn = op.get_bind()
    conn.execute(text("set @@lock_wait_timeout = 20;"))
    conn.execute(text("SET FOREIGN_KEY_CHECKS=0;"))
    conn.execute(text("ALTER TABLE event DROP CONSTRAINT imap_password_id_ifbk"))
    conn.execute(text("ALTER TABLE event DROP CONSTRAINT smtp_password_id_ifbk"))
    conn.execute(text("ALTER TABLE event DROP COLUMN imap_username"))
    conn.execute(text("ALTER TABLE event DROP COLUMN smtp_username"))
    conn.execute(text("ALTER TABLE event DROP COLUMN imap_password_id"))
    conn.execute(text("ALTER TABLE event DROP COLUMN smtp_password_id"))
