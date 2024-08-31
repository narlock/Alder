---
layout: page
title: API Specification
permalink: /api-spec/
---

<link rel="stylesheet" href="https://unpkg.com/swagger-ui-dist/swagger-ui.css">

<style>
  #swagger-ui {
    padding: 20px;
  }

  /* Set all text to white color */
  .swagger-ui .topbar, 
  .swagger-ui .info .title, 
  .swagger-ui .info .description,
  .swagger-ui .opblock-summary-description,
  .swagger-ui .opblock-summary-path,
  .swagger-ui .opblock-summary-method,
  .swagger-ui .response-col_status,
  .swagger-ui .response-col_description,
  .swagger-ui .response-col_links,
  .swagger-ui .opblock-tag,
  .swagger-ui .opblock-section-header h4,
  .swagger-ui .parameters-col_description,
  .swagger-ui .model-box,
  .swagger-ui .parameter__name, 
  .swagger-ui .parameter__in,
  .swagger-ui table thead tr th,
  .swagger-ui table tbody tr td,
  .swagger-ui .responses-inner h4,
  .swagger-ui .responses-inner table tbody tr td,
  .swagger-ui .responses-inner table thead tr th,
  .swagger-ui .model-title,
  .swagger-ui .property.primitive,
  .swagger-ui .model .model-title,
  .swagger-ui .model .property .property-type,
  .swagger-ui .opblock-summary {
    color: black !important;
  }

  /* Force endpoint text color to white */
  .swagger-ui .opblock-summary-method,
  .swagger-ui .opblock-summary-path {
    color: black !important;
  }

  /* Set background color of "Parameters" and "Responses" sections */
  .swagger-ui .opblock-section-header,
  .swagger-ui .parameters-container,
  .swagger-ui .responses-wrapper,
  .swagger-ui .opblock-description-wrapper,
  .swagger-ui .opblock-section {
    background-color: white; /* Match this to your body background color */
    color: black;
  }

  /* Modify the background color of table rows to make the white text stand out */
  .swagger-ui table tbody tr td, 
  .swagger-ui table thead tr th {
    background-color: white;
  }

  /* Ensure background color supports the white text */
  #swagger-ui {
    background-color: white;
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
