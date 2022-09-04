from flask import url_for


def get_tag_list(type=None, is_map=False):
    # creates a list of anchor tags, starting with the refresh button
    tag_list = []
    tag_list.append('<div class="nav-tags">')
    if is_map:
        refresh_url = url_for('maps.refresh_map', **{'type': type})
        tag_list.append('<a href="' + refresh_url + '">Refresh</a>')
    # adds anchor tags to the list for the other maps
    for other in ['cave', 'dungeon', 'world']:
        if other != type:
            map_url = url_for('maps.get_map', **{'type': other})
            tag_list.append(
                '<a href="' + map_url + '">' + other.capitalize() + '</a>'
                )

    load_url = url_for('maps.load')
    tag_list.append('<a href="' + load_url + '">Load</a>')
    if is_map:
        tag_list.append('''
            </div>
            <form class="save-form" method="post">
                <input type="submit" value="Save">
                <label for="mapname">Map Name:</label>
                <input name="mapname" id="mapname" required>
            </form>
        ''')
    return tag_list
