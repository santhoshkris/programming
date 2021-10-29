<?php

use App\Http\Controllers\BookController;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;

/*
|--------------------------------------------------------------------------
| API Routes
|--------------------------------------------------------------------------
|
| Here is where you can register API routes for your application. These
| routes are loaded by the RouteServiceProvider within a group which
| is assigned the "api" middleware group. Enjoy building your API!
|
*/

Route::middleware('auth:sanctum')->get('/user', function (Request $request) {
    return $request->user();
});

Route::get('/books/{id}', [BookController::class, 'getBook']);
Route::delete('/books/{id}', [BookController::class, 'deleteBook']);
Route::post('/books', [BookController::class, 'addBook']);
Route::put('/books/{id}', [BookController::class, 'updateBook']);
