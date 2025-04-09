---
layout: archive
title: "Papers"
permalink: /papers/
author_profile: true
---

{% if site.author.googlescholar %}
  <div class="wordwrap">You can find my articles on <a href="{{site.author.googlescholar}}">my Google Scholar profile</a>.</div>
{% endif %}

{% include base_path %}

{% for post in site.papers reversed %}
  {% include archive-single.html %}
{% endfor %}
