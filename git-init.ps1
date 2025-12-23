$repoName = Split-Path -Leaf (Get-Location)
$githubUser = "Zero-Ace5"

echo "# $repoName" >> README.md
git init
git add README.md
git commit -m "first commit"
git branch -M main
git remote add origin "https://github.com/$githubUser/$repoName.git"
git push -u origin main
