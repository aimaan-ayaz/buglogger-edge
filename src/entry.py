from workers import Response, WorkerEntrypoint #type: ignore
from urllib.parse import urlparse
from pathlib import Path

class Default(WorkerEntrypoint):
    async def fetch(self, request, env):
        
        pathname= urlparse(request.url).path

        if pathname =="/bug-log" and request.method == "POST":
            form = await request.form_data()
            title = form.get("title")
            description = form.get("description")
            severity = form.get("severity")

            query = (
                await self.env.bug_logs.prepare(
                    "INSERT INTO bugs (title, description, severity) VALUES (?, ?, ?);"
                )
                .bind(title, description, severity)
                .run()
            )
            return Response(
            "<p> Successfully Added Bug </p>"
        )

        if pathname =="/bug-load" and request.method == "GET":

            query = (
                await self.env.bug_logs.prepare(
                    "SELECT * FROM bugs"
                )
                .run()
            )
            html = ""
            for buglist in query.results:
                id = buglist.id
                title = buglist.Title
                description = buglist.Description
                severity = buglist.Severity
                html+= f"<div>{id}</div> <div>{title}</div> <div>{description}</div> <div>{severity}</div>"

            html = f"""<div id="allbugs">
                            <div class="grid">
                            <div class="header">S No.</div>
                            <div class="header">Title</div>
                            <div class="header">Description</div>
                            <div class="header">Severity</div>
                            {html}"""
            return Response(html)
    
        return await self.env.ASSETS.fetch(request)
    
        