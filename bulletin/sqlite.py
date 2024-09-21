import sqlite3

def sql_create_post(data):
    # connect to database
    con = sqlite3.connect('bulletin.db')
    cur = con.cursor()

    # check if tables exist and create them if not.
    cur.execute("""SELECT name FROM sqlite_master WHERE type='table' AND name='REQUESTTABLE';
    """)
    if cursor.fetchone() is None:
        createTables

    # add a new post
    cur.execute("""INSERT INTO REQUESTTABLE (
        post_author,
        post_title,
        post_content,
        post_tag,
        location_of_help,
        date_help_needed,
        start_time,
        end_time,
        confirm_by
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);""", (
        data.get('user_uid'),
        data.get('title'),
        data.get('content'),
        data.get('tag'),
        data.get('location'),
        data.get('date_help_needed'),
        data.get('start_time'),
        data.get('end_time'),
        data.get('confirm_by')))

    con.commit()
    con.close()

def sql_create_comment(post_id, data):
    # connect to database
    con = sqlite3.connect('bulletin.db')
    cur = con.cursor()

    # check if tables exist and create them if not.
    cur.execute("""
        SELECT name FROM sqlite_master WHERE type='table' AND name='REQUESTTABLE';
    """)
    if cursor.fetchone() is None:
        createTables

    # add a new comment
    cur.execute("""INSERT INTO COMMENTTABLE (post_uid, comment_author, comment_content)
        VALUES (?, ?, ?);""", (
        data.get('post_uid'),
        data.get('comment_author'),
        data.get('comment_content'),))
   
   # increment post comment count
    cursor.execute("UPDATE REQUESTTABLE SET comments = comments + 1 WHERE post_uid = ?", (post_id,))

    con.commit()
    con.close()

def sql_load_bulletin(sort_by=None, order='asc'):
    # connect to database
    con = sqlite3.connect('bulletin.db')
    cur = con.cursor()

    # check if tables exist and create them if not.
    cur.execute("""SELECT name FROM sqlite_master WHERE type='table' AND name='REQUESTTABLE';
    """)
    if cursor.fetchone() is None:
        createTables

    offset = 0 
    
    cursor.execute("""
        SELECT * FROM REQUESTTABLE 
        WHERE deleted = 0 AND resolved = 0 AND date_help_needed > ?
        LIMIT 20 OFFSET ?
    """, (datetime.now(), offset))

    con.commit()
    con.close()

def construct_query(sort_by, order, tag, current_time):
    # Start building the base query
    sql_query = "SELECT * FROM REQUESTTABLE WHERE deleted = 0 AND resolved = 0 AND date_help_needed > ?"
    params = [current_time]

    # Add tag filtering if tag is not 'none'
    if tag != 'none':
        sql_query += " AND post_tag = ?"
        params.append(tag)

    # Add sorting if sort_by is not 'none'
    if sort_by != 'none':
        sql_query += f" ORDER BY {sort_by} {order}"

    # Execute the query
    cur.execute(sql_query, params)
    results = cur.fetchall()
    
    return results

def sql_load_bulletin(sort_by=None, order='asc'):
    # connect to database
    con = sqlite3.connect('bulletin.db')
    cur = con.cursor()

    # check if tables exist and create them if not.
    cur.execute("""SELECT name FROM sqlite_master WHERE type='table' AND name='REQUESTTABLE';
    """)
    if cursor.fetchone() is None:
        createTables

    cur.execute(construct_query(data))

    con.commit()
    con.close()

    
    

def sql_delete_post(post_id):
    pass


def createTables():
    # connect to database
    con = sqlite3.connect('bulletin.db')
    cur = con.cursor()
    
    # create table for requests
    cur.execute("""CREATE TABLE REQUESTTABLE (
    post_uid INTEGER PRIMARY KEY AUTOINCREMENT,
    post_author INTEGER NOT NULL,
    post_title TEXT NOT NULL,
    post_content TEXT NOT NULL,
    post_tag TEXT DEFAULT 'others' CHECK (post_tag IN ('babysitting', 'tutoring', 'pickupchild', 'mealshare', 'needride', 'others')),
    post_creation_datetime DATETIME DEFAULT CURRENT_TIMESTAMP,
    location_of_help TEXT,
    date_help_needed TEXT NOT NULL,
    start_time TEXT,
    end_time TEXT,
    confirm_by DATETIME,
    resolved BOOLEAN DEFAULT FALSE,
    number_of_comments INTEGER DEFAULT 0
    deleted BOOLEAN DEFAULT FALSE);""")

    # create table for comments
    cur.execute("""CREATE TABLE COMMENTTABLE (
    comment_uid INTEGER PRIMARY KEY,
    post_uid INTEGER NOT NULL,          -- original post id
    comment_author INTEGER NOT NULL,
    comment_content TEXT NOT NULL,
    comment_creation_datetime DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (post_uid) REFERENCES REQUESTTABLE(post_uid) ON DELETE CASCADE);""")

    con.commit()
    con.close()

if __name__ == '__main__':
    app.run(debug=True)
