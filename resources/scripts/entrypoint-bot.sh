#!/bin/bash
set -e

echo "🔄 Bazaga ulanish kutilmoqda..."

# PostgreSQL tayyor bo'lishini kutish
until PGPASSWORD=2309 psql -h db -U postgres -d django -c '\q' 2>/dev/null; do
  echo "⏳ PostgreSQL kutilmoqda..."
  sleep 2
done

echo "✅ PostgreSQL tayyor!"

# Django migrationlari
echo "🔄 Django migrationlari tekshirilmoqda..."
python manage.py migrate --noinput || {
  echo "⚠️ Migration xatosi, lekin davom etamiz..."
}

# Bot faylini tekshirish
if [ ! -f "bot/main.py" ]; then
  echo "❌ bot/main.py fayli topilmadi!"
  exit 1
fi

echo "⚡ Bot ishga tushmoqda..."

# Development yoki Production rejimi
if [ "${DJANGO_ENV}" = "development" ]; then
  echo "🔧 Development mode: auto-reload yoqilgan"
  # watchfiles o'rnatilganligini tekshirish
  if command -v watchfiles &> /dev/null; then
    exec watchfiles --filter python "python -m bot.main"
  else
    echo "⚠️ watchfiles topilmadi, oddiy rejimda ishga tushmoqda"
    exec python -m bot.main
  fi
else
  echo "🚀 Production mode: bot ishga tushmoqda"
  exec python -m bot.main
fi