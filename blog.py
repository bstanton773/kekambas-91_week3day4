class Blog:
    def __init__(self):
        self.users = []
        self.posts = []
        self.current_user = None
        
    def _get_post_from_id(self, post_id):
        for post in self.posts:
            if post.id == int(post_id):
                return post
    
    # Method to add a new user to our blog
    def create_new_user(self):
        # Get user info from user input
        username = input('Please enter a username: ')
        if username in {u.username for u in self.users}:
            print(f"User with username {username} already exists")
        else:
            password = input('Please enter a password: ')
            # Create a new User instance with info from input
            new_user = User(username, password)
            # Add user instance to list of users on blog
            self.users.append(new_user)
            print(f"{new_user} has been created")
        
    # Method to log a user in
    def log_user_in(self):
        # Get user info from user input
        username = input('What is your username: ')
        password = input('What is your password: ')
        # Loop through the list of blog users
        for user in self.users:
            # Check if that user has the same username and password that were inputted
            if user.username == username and user.check_password(password):
                # If they do, set the blog's current user to that user and break
                self.current_user = user
                print(f"{user} has been logged in")
                break
        # If no users in our blog user list have the username and password then print it is incorrect
        else:
            print('Username and/or Password is incorrect')
            
    # Method to log a user out
    def log_user_out(self):
        self.current_user = None
        print("You have successfully logged out.")
        
    # Method to create a new blog post
    def create_a_post(self):
        # Check to make sure the user trying to create a post is logged in
        if self.current_user is not None:
            # Get title and body from user input
            title = input('Enter the title of your post: ').title()
            body = input('Enter the body of your post: ')
            # Create a new Post instance with user input
            new_post = Post(title, body, self.current_user)
            # Add post object to list of blog posts
            self.posts.append(new_post)
            print(f"{new_post.title} has been created.")
        else:
            # If user is not logged in, print that they need to be
            print('You must be logged in to perform this action')
            
    # Method to view all posts
    def view_posts(self):
        if self.posts:
            for post in self.posts:
                print(post)
        else:
            print("There are currently no posts for this blog :(")
            
    # Method to view a single post
    def view_post(self, post_id): 
        post = self._get_post_from_id(post_id)
        if post:
            print(post)
        else:
            print(f"Post with an id of {post_id} does not exist")
            
    # Method to edit a single post
    def edit_post(self, post_id):
        post_to_edit = self._get_post_from_id(post_id)
        # Check that a post exists
        if post_to_edit:
            # Check that the user is logged in AND that the logged in user is author of post
            if self.current_user is not None and self.current_user == post_to_edit.author:
                print(post_to_edit)
                # Ask user which part of the post they would like to edit
                edit_part = input('Would you like to edit the title, body, both, or exit? ')
                # Make sure the user chose an acceptable response
                while edit_part not in {'title', 'body', 'both', 'exit'}:
                    edit_part = input('Would you like to edit the title, body, both, or exit? ')
                if edit_part == 'exit':
                    return
                elif edit_part == 'both':
                    # Get new title and body 
                    new_title = input('Enter the new title: ')
                    new_body = input('Enter the new body: ')
                    post_to_edit.update(title=new_title, body=new_body)
                elif edit_part == 'title':
                    # Get new title 
                    new_title = input('Enter the new title: ')
                    post_to_edit.update(title=new_title)
                elif edit_part == 'body':
                    # Get new body 
                    new_body = input('Enter the new body: ')
                    post_to_edit.update(body=new_body)
                print(f"{post_to_edit.title} has been updated.")
            
            # If not author but user logged in
            elif self.current_user is not None:
                print('You do not have permission to update this post')
            # If not logged in at all
            else:
                print('You must be logged in to perform this action')
        else:
            print(f"Post with an id of {post_id} does not exist.")
            
    # Method to delete a post
    def delete_post(self, post_id):
        post_to_delete = self._get_post_from_id(post_id)
        if post_to_delete:
            # Check if user is logged in AND that user is author of the post to delete
            if self.current_user and self.current_user == post_to_delete.author:
                # Set blog post list to a new list of posts that does not include the post to delete 
                self.posts = [p for p in self.posts if p != post_to_delete]
                print(f"{post_to_delete.title} has been deleted")   
            # If not author but user logged in
            elif self.current_user:
                print('You do not have persmission to delete this post.')
            # If not logged in at all
            else:
                print('You must be logged in to perform this action')
        else:
            print(f"Post with an id of {post_id} does not exist.")
        
        
        
class User:
    
    id_counter = 1
    
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.id = User.id_counter
        User.id_counter += 1
        
    def __str__(self):
        return self.username
    
    def __repr__(self):
        return f"<User {self.id}|{self.username}>"
    
    def check_password(self, password_to_check):
        return self.password == password_to_check
    
    
class Post:
    
    id_counter = 1
    
    def __init__(self, title, body, author):
        """
        title -> str
        body -> str
        author -> User
        """
        self.title = title
        self.body = body
        self.author = author
        self.id = Post.id_counter
        Post.id_counter += 1
        
    def __str__(self):
        formatted_post = f"""
        {self.id} - {self.title.title()}
        By: {self.author}
        {self.body}
        """
        return formatted_post
    
    def __repr__(self):
        return f"<Post {self.id}|{self.title} by {self.author}>"
    
    def update(self, **kwargs):
        for key, value in kwargs.items():
            if key in {'title', 'body'}:
                setattr(self, key, value)
    


### Define function to run the blog
def run_blog():
    # Create an instance of the blog
    my_blog = Blog()
    # Keep looping while blog is 'running'
    while True:
        # if there is currently no user logged in
        if my_blog.current_user is None:
            print("1. Sign Up\n2. Log In\n3. View All Posts\n4. View Single Post\n5. Quit")
            to_do = input('What option would you like to do? ')
            while to_do not in {'1', '5', '2', '3', '4'}:
                to_do = input('Please choose either 1, 2, 3, 4 or 5 ')
            # clear_output()
            if to_do == '5':
                print('Thanks for checking out our blog! Bye!')
                break
            elif to_do == '1':
                my_blog.create_new_user()
            elif to_do == '2':
                my_blog.log_user_in()
            elif to_do == '3':
                my_blog.view_posts()
            elif to_do == '4':
                post_id = input('What is the id of the post you would like to view? ')
                my_blog.view_post(post_id)

        # If there is a user logged in
        else:
            print("1. Log Out\n2. Create A Post\n3. View All Posts\n4. View Single Post\n5. Edit a Post\n6. Delete a Post")
            to_do = input('What option would you like to do? ')
            while to_do not in {'1', '2', '3', '4', '5', '6'}:
                to_do = input('Please choose 1, 2, 3, 4, 5, or 6')
            # clear_output()
            if to_do == '1':
                my_blog.log_user_out()
            elif to_do == '2':
                my_blog.create_a_post()
            elif to_do == '3':
                my_blog.view_posts()
            elif to_do == '4':
                post_id = input('What is the id of the post you would like to view? ')
                my_blog.view_post(post_id)
            elif to_do == '5':
                post_id = input('What is the id of the post you would like to edit? ')
                my_blog.edit_post(post_id)
            elif to_do == '6':
                post_id = input('What is the id of the post you would like to delete? ')
                my_blog.delete_post(post_id)
                
                
# Execute the function
run_blog()
