
create table login(
    id serial primary key,
    email varchar(100) unique NOT NULL,
    password varchar(30) NOT NULL,
    last_login TIMESTAMP 
);

create table account(
    id serial primary key,
    user_id int NOT NULL,
    name varchar(200) NOT NULL,
    user_name varchar(100) NOT NULL,
    birth_date date,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    foreign key (user_id) REFERENCES login (id)
);

create table roles(
    id serial primary key,
    role_name varchar(50)
)

create table account_role(
    user_id int not null,
    role_id int not null,
    grant_date TIMESTAMP NOT NULL,
    primary key (user_id, role_id),
    foreign key (role_id) REFERENCES roles (id),
    foreign key (user_id) REFERENCES account (id)
)


create table follower(
    id serial primary key,
    user_id int NOT NULL,
    follow_id int NOT NULL,
    foreign key (user_id) REFERENCES login (id),
    foreign key (follow_id) REFERENCES login (id),
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
)

create table photo_profile(
    id serial primary key,
    user_id int NOT NULL,
    description varchar(1000) NOT NULL,
    foreign key (user_id) REFERENCES login (id),
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
)

create table publication(
    id serial primary key,
    profile_id int NOT NULL,
    description varchar(1000),
    image varchar(100),
    foreign key (profile_id) REFERENCES profile (id),
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
)

create table comment(
    id serial primary key,
    publication_id int NOT NULL,
    description varchar(1000) NOT NULL,
    foreign key (publication_id) REFERENCES publication (id),
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
)

create table reactions(
    id serial primary key,
    emoticon varchar(100),
    name varchar(50),
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
)

create table reaction_post(
    id serial primary key,
    publication_id int NOT NULL,
    reaction_id int NOT NULL,
    foreign key (publication_id) REFERENCES publication (id),
    foreign key (reaction_id) REFERENCES reactions (id),
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL
)
