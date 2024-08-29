---
layout: page
title: API Specification
permalink: /api-spec/
---

<link rel="stylesheet" href="https://unpkg.com/swagger-ui-dist/swagger-ui.css">

<style>
  #swagger-ui {
    background-color: white;
    padding: 20px;
  }
</style>

The following API specification documents the different HTTP endpoints offered by the Alder API to communicate with the MySQL database.

<div id="swagger-ui"></div>

<script src="https://unpkg.com/swagger-ui-dist/swagger-ui-bundle.js"></script>
<script src="https://unpkg.com/swagger-ui-dist/swagger-ui-standalone-preset.js"></script>
<script>
  const ui = SwaggerUIBundle({
    url: "{{ site.baseurl }}/api-spec/spec.yaml",
    dom_id: '#swagger-ui',
    presets: [
      SwaggerUIBundle.presets.apis,
      SwaggerUIStandalonePreset
    ],
    layout: "StandaloneLayout",
    supportedSubmitMethods: [] // Disables "Try it out"
  })
</script>
