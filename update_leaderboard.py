import requests
import os

def get_contributors(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}/contributors"
    headers = {
        "Authorization": f"token {os.getenv('GITHUB_TOKEN')}"
    }  # Use GitHub token for authentication
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        contributors = response.json()
        leaderboard = []

        for contributor in contributors:
            leaderboard.append({
                "username": contributor["login"],
                "contributions": contributor["contributions"],
                "avatar_url": contributor["avatar_url"]
            })

        return sorted(leaderboard, key=lambda x: x["contributions"], reverse=True)
    else:
        print(f"Failed to fetch contributors: {response.status_code}, {response.text}")
        return []

def generate_html(leaderboard, owner, repo):
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{repo} Leaderboard</title>
        <style>
            body {{ 
                background: linear-gradient(0deg, #1b2838, #1e3a4c, #1f4c60, #16202b);
                background-size: 300% 300%;
                animation: gradient 30s ease infinite;
                font-family: Arial, sans-serif; 
                margin: 0;
                padding: 0;
                height: 100vh;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: flex-start;
                overflow: hidden;
            }}

            @keyframes gradient {{
                0% {{
                    background-position: 50% 0%;
                }}
                50% {{
                    background-position: 50% 100%;
                }}
                100% {{
                    background-position: 50% 0%;
                }}
            }}

            table {{ border-collapse: collapse; width: 80%; margin-top: 20px; z-index: 1; position: relative; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
            th {{ background-color: #f2f2f2; }}
            .avatar {{
                width: 40px;
                height: 40px;
                border-radius: 50%;
                margin-right: 10px;
                vertical-align: middle;
            }}
            h1 {{
                color: white;
                text-align: center;
                margin-top: 20px;
                z-index: 1;
                position: relative;
            }}
        </style>
    </head>
    <body>
        <h1>{repo} Leaderboard</h1>
        <table>
            <thead>
                <tr>
                    <th>Rank</th>
                    <th>Contributor</th>
                    <th>Contributions</th>
                </tr>
            </thead>
            <tbody>
    """
    for rank, contributor in enumerate(leaderboard, start=1):
        html += f"""
                <tr>
                    <td>{rank}</td>
                    <td><img src='{contributor['avatar_url']}' alt='Avatar' class='avatar'>{contributor['username']}</td>
                    <td>{contributor['contributions']}</td>
                </tr>
        """
    html += """
            </tbody>
        </table>
    </body>
    </html>
    """
    return html

def save_html_to_file(html, filename="leaderboard.html"):
    with open(filename, "w") as file:
        file.write(html)

def update_readme(leaderboard, repo):
    top_5 = leaderboard[:5]
    markdown = f"# {repo} Top 5 Contributors\n\n"
    markdown += "| Rank | Contributor | Contributions |\n"
    markdown += "|------|-------------|----------------|\n"
    for rank, contributor in enumerate(top_5, start=1):
        markdown += (
            f"| {rank} | "
            f"<img src='{contributor['avatar_url']}' alt='{contributor['username']}' width='40'> "
            f"{contributor['username']} | {contributor['contributions']} |\n"
        )

    try:
        with open("README.md", "r") as file:
            content = file.readlines()

        with open("README.md", "w") as file:
            updated = False
            for line in content:
                if line.strip() == "<!-- LEADERBOARD START -->":
                    file.write("<!-- LEADERBOARD START -->\n")
                    file.write(markdown)
                    file.write("\n<!-- LEADERBOARD END -->\n")
                    updated = True
                elif not (line.strip() == "<!-- LEADERBOARD END -->"):
                    file.write(line)

            if not updated:
                file.write("\n<!-- LEADERBOARD START -->\n")
                file.write(markdown)
                file.write("\n<!-- LEADERBOARD END -->\n")

        print("README.md updated successfully with the Top 5 leaderboard.")
    except FileNotFoundError:
        print("README.md not found. Creating a new one.")
        with open("README.md", "w") as file:
            file.write(markdown)

if __name__ == "__main__":
    owner = input("Enter the GitHub repository owner: ")
    repo = input("Enter the GitHub repository name: ")

    print("Generating GitHub repository leaderboard...")

    leaderboard = get_contributors(owner, repo)

    if leaderboard:
        html = generate_html(leaderboard, owner, repo)
        save_html_to_file(html)
        update_readme(leaderboard, repo)
        print("Leaderboard HTML and README updated successfully.")
    else:
        print("No contributors found or failed to retrieve data.")
