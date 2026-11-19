# Wiki pages

These Markdown pages are written for the GitHub wiki. The wiki is a separate git repository (`ghostlight-node.wiki.git`) that GitHub only creates after you save a first page in the web UI. To publish: create any page in the Wiki tab once, then

```
git clone https://github.com/DefeatedWarrior/ghostlight-node.wiki.git
cp wiki/*.md ghostlight-node.wiki/   # skip this README
cd ghostlight-node.wiki && git add -A && git commit -m "Add wiki" && git push
```
