#!/bin/bash

set -e

# Directory to store logs and tracking data
LOGS_DIR="github-action-logs"
TRACKING_FILE="$LOGS_DIR/.downloaded_runs"

# Create logs directory if it doesn't exist
mkdir -p "$LOGS_DIR"

# Create tracking file if it doesn't exist
touch "$TRACKING_FILE"

echo "Fetching GitHub Actions runs..."

# Get all runs (limit to last 100)
all_runs=$(gh run list --limit 100 --json databaseId,name,conclusion,status,createdAt,headBranch --jq '.[]')

if [ -z "$all_runs" ] || [ "$all_runs" = "null" ]; then
    echo "Error: No runs found"
    exit 1
fi

# Count total runs
total_runs=$(echo "$all_runs" | jq -s 'length')
echo "Found $total_runs run(s)"
echo ""

# Track statistics
new_count=0
updated_count=0
skipped_count=0

# Process each run
echo "$all_runs" | jq -c '.' | while IFS= read -r run; do
    run_id=$(echo "$run" | jq -r '.databaseId')
    run_name=$(echo "$run" | jq -r '.name')
    conclusion=$(echo "$run" | jq -r '.conclusion // "in_progress"')
    status=$(echo "$run" | jq -r '.status')
    branch=$(echo "$run" | jq -r '.headBranch')
    created_at=$(echo "$run" | jq -r '.createdAt')

    # Generate consistent filename for this run ID
    output_file="$LOGS_DIR/run-${run_id}.txt"

    # Check if we've already downloaded this run
    if grep -q "^${run_id}:" "$TRACKING_FILE"; then
        # Get the stored status
        stored_status=$(grep "^${run_id}:" "$TRACKING_FILE" | cut -d: -f2)

        # If the run was incomplete and is now complete, update it
        if [ "$stored_status" = "in_progress" ] && [ "$status" = "completed" ]; then
            echo "Updating run $run_id (now completed)"
            echo "  Name: $run_name"
            echo "  Branch: $branch"
            echo "  Status: $status ($conclusion)"

            # Download the logs
            if gh run view "$run_id" --log > "$output_file" 2>/dev/null; then
                # Update tracking file
                sed -i.bak "/^${run_id}:/d" "$TRACKING_FILE"
                echo "${run_id}:${status}:${created_at}" >> "$TRACKING_FILE"
                updated_count=$((updated_count + 1))
                echo "  ✓ Updated: $output_file"
            else
                echo "  ✗ Failed to download logs"
            fi
            echo ""
        else
            # Already downloaded and status hasn't changed meaningfully
            skipped_count=$((skipped_count + 1))
        fi
    else
        # New run, download it
        echo "Downloading new run $run_id"
        echo "  Name: $run_name"
        echo "  Branch: $branch"
        echo "  Status: $status ($conclusion)"
        echo "  Created: $created_at"

        # Download the logs
        if gh run view "$run_id" --log > "$output_file" 2>/dev/null; then
            # Add to tracking file
            echo "${run_id}:${status}:${created_at}" >> "$TRACKING_FILE"
            new_count=$((new_count + 1))

            # Show file info
            file_size=$(du -h "$output_file" | cut -f1)
            line_count=$(wc -l < "$output_file")
            echo "  ✓ Downloaded: $output_file"
            echo "    Size: $file_size, Lines: $line_count"
        else
            echo "  ✗ Failed to download logs"
        fi
        echo ""
    fi
done

echo "==============================================="
echo "Summary:"
echo "  New logs downloaded: $new_count"
echo "  Updated logs: $updated_count"
echo "  Skipped (already current): $skipped_count"
echo "  Total runs processed: $total_runs"
echo ""
echo "All logs are stored in: $LOGS_DIR/"
echo ""
echo "To view a specific log:"
echo "  cat $LOGS_DIR/run-<RUN_ID>.txt"
echo "  # or"
echo "  less $LOGS_DIR/run-<RUN_ID>.txt"
