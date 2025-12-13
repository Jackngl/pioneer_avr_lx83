#!/bin/bash
# Script to add GitHub topics to the repository

REPO_OWNER="Jackngl"
REPO_NAME="pioneer_avr_lx83"

# Topics to add
TOPICS='["home-assistant","homeassistant","hacs","custom-component","integration","pioneer","avr","amplifier","home-automation","iot"]'

# Get token from environment or file
if [ -n "$GITHUB_TOKEN" ]; then
    TOKEN="$GITHUB_TOKEN"
elif [ -f ~/.github_token ]; then
    TOKEN=$(cat ~/.github_token | tr -d '\n')
elif [ -f .github_token ]; then
    TOKEN=$(cat .github_token | tr -d '\n')
else
    echo "❌ Error: GitHub token not found!"
    echo ""
    echo "Please provide a GitHub token in one of these ways:"
    echo "1. Set GITHUB_TOKEN environment variable:"
    echo "   export GITHUB_TOKEN=your_token_here"
    echo "2. Create a file ~/.github_token with your token"
    echo "3. Create a file .github_token in the project root"
    echo ""
    echo "To create a token:"
    echo "1. Go to https://github.com/settings/tokens/new"
    echo "2. Click 'Generate new token (classic)'"
    echo "3. Select scope: 'public_repo'"
    echo "4. Copy the token and use it as described above"
    exit 1
fi

echo "📋 Adding topics to ${REPO_OWNER}/${REPO_NAME}..."
echo ""

# Get current topics
echo "Fetching current topics..."
CURRENT_TOPICS=$(curl -s -H "Accept: application/vnd.github.mercy-preview+json" \
    -H "Authorization: token ${TOKEN}" \
    "https://api.github.com/repos/${REPO_OWNER}/${REPO_NAME}/topics" | \
    grep -o '"names":\[[^]]*\]' | sed 's/"names":\[\(.*\)\]/\1/' | sed 's/"//g')

if [ -n "$CURRENT_TOPICS" ]; then
    echo "Current topics: $CURRENT_TOPICS"
else
    echo "Current topics: None"
fi
echo ""

# Set topics
echo "Setting topics..."
RESPONSE=$(curl -s -w "\n%{http_code}" -X PUT \
    -H "Accept: application/vnd.github.mercy-preview+json" \
    -H "Authorization: token ${TOKEN}" \
    -H "Content-Type: application/json" \
    -d "{\"names\":${TOPICS}}" \
    "https://api.github.com/repos/${REPO_OWNER}/${REPO_NAME}/topics")

HTTP_CODE=$(echo "$RESPONSE" | tail -n1)
BODY=$(echo "$RESPONSE" | head -n-1)

if [ "$HTTP_CODE" = "200" ]; then
    echo "✅ Topics successfully updated!"
    echo ""
    echo "Repository: https://github.com/${REPO_OWNER}/${REPO_NAME}"
    echo "You can verify the topics on the repository page."
else
    echo "❌ Failed to update topics."
    echo "HTTP Code: $HTTP_CODE"
    echo "Response: $BODY"
    exit 1
fi

