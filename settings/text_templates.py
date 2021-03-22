# Common Handlers Text Templates
hello_msg = ("Hello, {user_name}, you started me.\n"
             "I am the bot that allows you to get Instagram content "
             "by link you sent me.\n\n"
             "For more information use /help command.")

help_text = ("List of Commands:\n"
             "/start — Start the bot;\n"
             "/help — This help message;\n\n"
             "Currently, you can send me <strong>two types of links</strong>:\n"
             "1. A <strong>profile link</strong> that will allow you to get the user's "
             "<strong>last 12 posts</strong> and available <strong>stories</strong>. "
             "The link must match the following template: "
             "<pre>https://www.instagram.com/username/</pre>\n"
             "2. The post link, that will allow you to get some "
             "information about current post and all content that the post contains."
             "The link must match the following template: "
             "<pre>https://www.instagram.com/p or tv/post_shortcode/</pre>\n\n"
             "If you want to use me, you have to <strong>follow for some rules:</strong>\n"
             "1. Make sure that the profile you are sending me a link to is "
             "<strong>not private</strong>;\n"
             "2. may be something else...")

# Instagram Handlers Text Templates
profile_caption = ("<strong>Full Name</strong>: <pre>{full_name}</pre>\n———\n"
                   "<strong>Bio</strong>: <pre>{bio}</pre>\n———\n"
                   "<strong>Is Private</strong>: <pre>{is_private}</pre>\n———\n"
                   "<strong>Followers</strong>: <pre>{followers}</pre>\n———\n"
                   "<strong>Follow</strong>: <pre>{follow}</pre>\n———\n"
                   "<strong>Category</strong>: <pre>{category}</pre>\n———\n"
                   "<strong>Posts Count</strong>: <pre>{posts}</pre>\n———\n"
                   "<strong>IGTV Count</strong>: <pre>{igtvs}</pre>\n———\n"
                   "<strong>Highlights Count</strong>: <pre>{highlights}</pre>\n")

post_caption = ("<strong>Description</strong>: <pre>{description}</pre>\n———\n"
                "<strong>Likes</strong>: <pre>{likes}</pre>\n———\n"
                "<strong>Comments</strong>: <pre>{comments}</pre>\n———\n")

error_post_caption = ("I can`t send you this."
                      "Here is a <a href='{post_content}'>Link</a>\n"
                      "{caption}")

not_found_error_text = "I got an empty response. There is no such post or the profile is private. Read /help."
not_found_profile_text = "{url} — {error}"

private_profile_text = "This profile is private. Read /help"

no_stories_text = "Sorry, but the user doesn't seem to have any stories..."
no_posts_text = "Sorry, but the user doesn't seem to have any posts..."

# Admin Handlers Text Templates
