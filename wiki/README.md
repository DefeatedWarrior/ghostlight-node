# Wiki pages

These pages are the source for the GitHub wiki. The wiki is a separate repo (`ghostlight-node.wiki.git`) created only after the first page is saved in the web UI.

```
git clone https://github.com/DefeatedWarrior/ghostlight-node.wiki.git
cp wiki/*.md ghostlight-node.wiki/
rm ghostlight-node.wiki/README.md
cd ghostlight-node.wiki && git add -A && git commit -m "Wiki" && git push
```

Page links use `[[Page Name]]` and need the file names to match (spaces become hyphens), which they do.
