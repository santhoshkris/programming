<?php

include_once "Book.php";
class Model
{
    public function getBookList()
    {
        return array(
            "Jurassic Park" => new Book("Jurassic Park", "Michael Crichton", ""),
            "Moonwalker" => new Book("Moonwalker", "J. Walker", ""),
            "PHP for Dummies" => new Book("PHP for Dummies", "Some Smart Guy", "")
        );
    }
    public function getBook($title)
    {
        $allBooks = $this->getBookList();
        return $allBooks[$title];
    }
}
