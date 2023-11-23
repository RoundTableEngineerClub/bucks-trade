DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS post;

CREATE TABLE user_info (
    UniqueID INT PRIMARY KEY,
    gender VARCHAR(255),
    personalDescription VARCHAR(255),
    creditRating INT
);

CREATE TABLE user_auth (
    id INT(10) PRIMARY KEY,
    username VARCHAR(255) UNIQUE,
    password VARCHAR(255),
    email VARCHAR(255) UNIQUE,
    storageId INT(10),
    FOREIGN KEY (storageId) REFERENCES storage(storageId)
);

CREATE TABLE user_data (
    UniqueID INT PRIMARY KEY,
    email VARCHAR(255) UNIQUE,
    phoneNumber INT(10),
    storageId INT(10),
    FOREIGN KEY (storageId) REFERENCES storage(stroageId)
);


CREATE TABLE storage (
    storageId INT(10) PRIMARY KEY,
);

CREATE TABLE product (
    UniqueID INT(10) PRIMARY KEY,
    description VARCHAR(255),
    imgURL VARCHAR(255),
    price DOUBLE(50),
    tagId INT(10),
);

CREATE TABLE product_list (
    id INT AUTO_INCREMENT PRIMARY KEY,
    storageId INT(10),
    productId INT(10),
    FOREIGN KEY (storageId) REFERENCES storage(storageId),
    FOREIGN KEY (productId) REFERENCES product(UniqueID)
);

CREATE TABLE tag (
    id INT AUTO_INCREMENT PRIMARY KEY,
    UniqueID INT(10),
    tagDes VARCHAR(255),
    FOREIGN KEY (UniqueID) REFERENCES product(UniqueID)
);