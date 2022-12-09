
create table user(
    id serial primary key,
    email varchar(100) unique NOT NULL,
    password varchar(30) NOT NULL,
)

create table profile(
    id serial primary key,
    user_id int NOT NULL,
    name varchar(200) NOT NULL,
    user_name varchar(100) NOT NULL,
    birth_date date,
    foreign key (user_id) REFERENCES user (id)
    create_at date,
    update_at date,
)

create table follower(
    id serial primary key,
    user_id int NOT NULL,
    follow_id int NOT NULL,
    foreign key (user_id) REFERENCES user (id),
    foreign key (follow_id) REFERENCES user (id),
    create_at date,
    update_at date,
)

create table photo_profile(
    id serial primary key,
    user_id int NOT NULL,
    description varchar(1000) NOT NULL,
    foreign key (user_id) REFERENCES user (id),
    create_at date,
    update_at date,
)

create table publication(
    id serial primary key,
    profile_id int NOT NULL,
    description varchar(1000),
    image varchar(100),
    foreign key (profile_id) REFERENCES profile (id),
    create_at date,
    update_at date,
)

create table comment(
    id serial primary key,
    publication_id int NOT NULL,
    description varchar(1000) NOT NULL,
    foreign key (publication_id) REFERENCES publication (id),
    create_at date,
    update_at date,
)

create table reactions(
    id serial primary key,
    emoticon varchar(100),
    name varchar(50),
    create_at date,
    update_at date,
)

create table reaction_post(
    id serial primary key,
    publication_id int NOT NULL,
    reaction_id int NOT NULL,
    foreign key (publication_id) REFERENCES publication (id),
    foreign key (reaction_id) REFERENCES reactions (id),
    create_at date,
    update_at date,
)
