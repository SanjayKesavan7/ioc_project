import json
import os

def recover_files(transcript_path):
    print(f"Recovering from {transcript_path}")
    if not os.path.exists(transcript_path):
        print("Path not found!")
        return

    with open(transcript_path, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                data = json.loads(line)
                if 'tool_calls' in data:
                    for tc in data['tool_calls']:
                        name = tc.get('name')
                        args = tc.get('args', {})
                        if isinstance(args, str):
                            try:
                                args = json.loads(args)
                            except:
                                continue
                                
                        if name == 'default_api:write_to_file' or name == 'write_to_file':
                            filepath = args.get('TargetFile')
                            content = args.get('CodeContent')
                            if filepath and content:
                                # Ensure we extract just the real path (it might have file:/// prefix)
                                if filepath.startswith('file:///'):
                                    filepath = filepath.replace('file:///', '')
                                os.makedirs(os.path.dirname(filepath), exist_ok=True)
                                with open(filepath, 'w', encoding='utf-8') as out:
                                    out.write(content)
                                print(f"Recovered: {filepath}")
                        elif name == 'default_api:replace_file_content' or name == 'replace_file_content':
                            filepath = args.get('TargetFile')
                            target = args.get('TargetContent')
                            replacement = args.get('ReplacementContent')
                            if filepath and target and replacement and os.path.exists(filepath):
                                if filepath.startswith('file:///'):
                                    filepath = filepath.replace('file:///', '')
                                with open(filepath, 'r', encoding='utf-8') as cur:
                                    current_content = cur.read()
                                new_content = current_content.replace(target, replacement)
                                with open(filepath, 'w', encoding='utf-8') as out:
                                    out.write(new_content)
                                print(f"Patched: {filepath}")
            except Exception as e:
                pass

brain_dir = r"C:\Users\sanja\.gemini\antigravity\brain\1e96e356-70e8-4b2b-a1be-ecd0eb57c766"
main_transcript = os.path.join(brain_dir, ".system_generated", "logs", "transcript_full.jsonl")
recover_files(main_transcript)

subagent_dir = r"C:\Users\sanja\.gemini\antigravity\brain\4ae52170-096f-4192-bef5-4d7741bca4aa"
sub_transcript = os.path.join(subagent_dir, ".system_generated", "logs", "transcript_full.jsonl")
recover_files(sub_transcript)
