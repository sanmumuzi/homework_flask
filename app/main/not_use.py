# < div
#
#
# class ="post-thumbnail" >
#
# < img
#
#
# class ="img-rounded profile-thumbnail"
#
#
# src = "{{ url_for('static', filename='image/Python.png') }}" >
# < / div >

# < div
#
#
# class ="post-body" >
#
#
# { % if post.body_html %}
# {{post.body_html | safe}}
# { % else %}
# {{post.body}}
# { % endif %}
# < / div >
