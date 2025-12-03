#!/bin/bash
set -e

echo "🔄 Bazaga ulanish kutilmoqda..."
until PGPASSWORD=2309 psql -h db -U postgres -d django -c '\q' 2>/dev/null; do
  echo "⏳ PostgreSQL kutilmoqda..."
  sleep 2
done
echo "✅ PostgreSQL tayyor!"

echo "🔄 Django migrationlari tekshirilmoqda..."
python manage.py migrate --noinput || true

echo "⚡ Bot ishga tushmoqda..."

if [ "${DJANGO_ENV}" = "development" ]; then
  echo "🔧 Development mode: auto-reload yoqilgan"
  exec watchfiles --filter python "python -m bot.main"
else
  echo "🚀 Production mode: bot ishga tushmoqda"
  exec python -m bot.main
fi