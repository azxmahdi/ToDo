{* tempaltes/email/send-mail-confirm.tpl *}
{% extends "mail_templated/base.tpl" %}

{% block subject %}
account configuration
{% endblock %}


{% block html %}
<h1>Please click on the link below to verify your account</h1>

<a href="{{ url }}" 
   style="background-color: #4CAF50; border: none; color: white; padding: 15px 32px; text-align: center; text-decoration: none; display: inline-block; font-size: 16px; margin: 4px 2px; cursor: pointer; border-radius: 12px; transition: background-color 0.3s;">
   verify
</a>

{% endblock %}