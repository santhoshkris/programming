<?php

namespace App\Http\Controllers;

use App\Exceptions\InvalidMeterIdException;
use App\Services\MeterReadingService;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;

class MeterReadingController extends Controller
{

    private $meterReadingService;

    public function __construct(MeterReadingService $meterReadingService)
    {
        $this->meterReadingService = $meterReadingService;
    }

    /**
     * @OA\Get(
     *    path="/readings/read/{smartMeterId}",
     *    operationId="getReading",
     *    tags={"getReadings"},
     *    summary="Get all electricity readings",
     *    description="Returns list of electricity readings",
     *    @OA\Parameter(
     *        name="smartMeterId",
     *        description="SmartMeter id",
     *        required=true,
     *        in="path",
     *        @OA\Schema(
     *            type="string"
     *        )
     *      ),
     *    @OA\Response(
     *        response=200,
     *        description="successful operation",
     *        @OA\JsonContent(
     *             type="array",
     *                @OA\Items(
     *                      @OA\Property(
     *                         property="time",
     *                         type="string",
     *                         example="2020-11-29T08:00:00Z"
     *                      ),
     *                      @OA\Property(
     *                         property="reading",
     *                         type="number",
     *                         format="double",
     *                         example=0.0621
     *                      ),
     *                ),
     *        ),
     *     ),
     *    @OA\Response(response=400, description="Bad request"),
     *    )
     *
     * Returns all electricity readings for the given smart meter
     */

    public function getReading($smartMeterId): JsonResponse
    {
        try {
            $electricityReadings = $this->meterReadingService->getReadings($smartMeterId);
            return response()->json($electricityReadings);
        } catch (InvalidMeterIdException $exception) {
            return response()->json($exception->getMessage());
        }
    }



    /**
     * @OA\POST(
     *     path="/readings/store",
     *     summary="Store electricity readings for a smartmeter",
     *     tags={"storeReadings"},
     *     @OA\RequestBody(
     *        required = true,
     *        description = "SmartMeter and Electricity Readings",
     *        @OA\JsonContent(
     *             type="object",
     *             @OA\Property(
     *                property="smartMeterId",
     *                type="string",
     *                example="smart-meter-1"
     *             ),
     *             @OA\Property(
     *                property="electricityReadings",
     *                type="array",
     *                example={{
     *                  "time": "<time>",
     *                  "reading": "<reading>",
     *                }, {
     *                  "time": "2020-11-29T08:00:00Z",
     *                  "reading": 0.0503,
     *                }},
     *                @OA\Items(
     *                      @OA\Property(
     *                         property="time",
     *                         type="string",
     *                         example="2020-11-29T08:00:00Z"
     *                      ),
     *                      @OA\Property(
     *                         property="reading",
     *                         type="number",
     *                         format="double",
     *                         example=0.0567
     *                      ),
     *                ),
     *             ),
     *        ),
     *     ),
     *
     *
     *     @OA\Response(
     *        response="200",
     *        description="Successful response",
     *     ),
     * )
     */

    public function storeReadings(Request $request): JsonResponse
    {
        try {
            $isReadingsStored = $this->meterReadingService->storeReadings($request->all()["smartMeterId"], $request->all()["electricityReadings"]);
        } catch (InvalidMeterIdException $exception) {
            return response()->json($exception->getMessage());
        }
        if ($isReadingsStored) {
            return response()->json("Readings inserted successfully", 201);
        }

        return response()->json("No readings available to insert");
    }
}
