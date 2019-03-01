echo "System Initializing..."
echo ""
echo "Setting LAST-START TAG"
sh tags_api/set-device-tag.sh "STATUS_last_start" $(date '+%Y-%m-%d %H:%M:%S')

echo "Starting Application"
python3 src/main.py