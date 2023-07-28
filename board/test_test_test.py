"""

   {% if page_obj.has_previous %}
       <a href="?page=1">1</a>
       {% if page_obj.previous_page_number != 1 %}
           ...
           <a href="?page={{ page_obj.previous_page_number }}">{{ page_obj.previous_page_number }}</a>
       {% endif %}
   {% endif %}

   {# Информация о текущей странице #}
   {{ page_obj.number }}

   {# Информация о следующих страницах #}
   {% if page_obj.has_next %}
       <a href="?page={{ page_obj.next_page_number }}">{{ page_obj.next_page_number }}</a>
       {% if paginator.num_pages != page_obj.next_page_number %}
           ...
           <a href="?page={{ page_obj.paginator.num_pages }}">{{ page_obj.paginator.num_pages }}</a>
       {% endif %}
   {% endif %}

"""


'''
249917283107-gua14fg959o0afhpform6vbjj1ub31mi.apps.googleusercontent.com
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
'''


'''
{% load spurl %}

{% if page_obj.has_previous %}
<a href="{% spurl query=request.GET set_query='page={{ 1 }}'%}">{{ 1 }}</a>
{% if page_obj.previous_page_number != 1 %}
...
<a href="{% spurl query=request.GET set_query='page={{ page_obj.previous_page_number }}'%}">{{ page_obj.previous_page_number }}</a>
{% endif %}
{% endif %}

{{ page_obj.number }}

{% if page_obj.has_next %}
<a href="{% spurl query=request.GET set_query='page={{ page_obj.next_page_number }}'%}">{{ page_obj.next_page_number }}</a>
{% if paginator.num_pages != page_obj.next_page_number %}
...
<a href="{% spurl query=request.GET set_query='page={{ page_obj.paginator.num_pages }}'%}">{{ page_obj.paginator.num_pages }}</a>
{% endif %}
{% endif %}



   {% if page_obj.has_previous %}
        <a class="page-link" href="{% spurl query=request.GET set_query='page=1'%}">1</a>
       {# <a href="?page=1">1</a>#}
       {% if page_obj.previous_page_number != 1 %}
           ...
           <a href="?page={{ page_obj.previous_page_number }}">{{ page_obj.previous_page_number }}</a>
       {% endif %}
   {% endif %}

   {# Информация о текущей странице #}
   {{ page_obj.number }}

   {# Информация о следующих страницах #}
   {% if page_obj.has_next %}
       <a href="?page={{ page_obj.next_page_number }}">{{ page_obj.next_page_number }}</a>
       {% if paginator.num_pages != page_obj.next_page_number %}
           ...
           <a href="?page={{ page_obj.paginator.num_pages }}">{{ page_obj.paginator.num_pages }}</a>
       {% endif %}
   {% endif %}





<form action="{{post.id}}/response/">
    <button type="submit"> Оставить комментарий</button>
</form>

<form action="{{post.id}}/all_responses/">
    <button type="submit"> Посмотреть все комментарии</button>
</form>

<br>
<br>
{% for category in post.category.values %}

<form method="GET" name="callback" action="sign_me/">
    {% csrf_token %}
  <input type="hidden" name="category" value="{{ category.cat_name }}">
  <button type="submit" name="Подписаться"> Подписаться на новости  по теме {{ category.cat_name }}!</button>
     <br>
</form>

{%endfor%}



<h1>Комментарий к посту {{ response.post.post_name}}</h1>
 от {{ response.post.time_in | date:"DATETIME_FORMAT"}} <br>
{% for category in post.category.values %}
    {{ category.cat_name }} <br>
{%endfor%}
{{ response.text}} <br>
<br>
<br>

<br>
<br>
<br>
{%if response.post.author == user%}
<form action="{{response.post.id}}/update/">
    <button type="submit"> Изменить комментарий</button>
</form>
<form action="{{response.post.id}}/response/delete/">
    <button type="submit"> Удалить комментарий</button>
</form>
{%endif%}
'''