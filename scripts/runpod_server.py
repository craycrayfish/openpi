import runpod
import time
from .serve_policy import create_policy, Args
from openpi.policies import policy as _policy

def process_image_chunk(chunk_data, chunk_number, total_chunks):
    """
    Simulate processing a chunk of image data.
    In a real application, you might do actual image processing here.
    """
    return {
        "chunk_number": chunk_number,
        "chunk_size": len(chunk_data),
        "processed_at": time.strftime("%H:%M:%S")
    }

def aloha_sim_handler(job):
    """
    Handler that responds to a request with an action using the appropriate policy.
    """
    job_input = job["input"]

    args = job_input.get("policy_args", Args())
    policy = create_policy(args)
    # Record the policy's behavior.
    if args.record:
        policy = _policy.PolicyRecorder(policy, "policy_records")


    
    # Get the base64 string from input
    base64_string = job_input.get("base64_image")
    if not base64_string:
        yield {"error": "No base64_image provided in input"}
        return

    try:
        # Decode base64 string
        image_data = base64.b64decode(base64_string)
        
        # Open image to validate and get info
        image = Image.open(io.BytesIO(image_data))
        
        # Get image info for initial metadata
        yield {
            "status": "started",
            "image_info": {
                "format": image.format,
                "size": image.size,
                "mode": image.mode
            }
        }

        # Simulate processing image in chunks
        # In a real application, you might process different parts of the image
        chunk_size = len(image_data) // 4  # Process in 4 chunks
        total_chunks = (len(image_data) + chunk_size - 1) // chunk_size

        for i in range(total_chunks):
            start_idx = i * chunk_size
            end_idx = min(start_idx + chunk_size, len(image_data))
            chunk = image_data[start_idx:end_idx]

            # Process this chunk
            result = process_image_chunk(chunk, i + 1, total_chunks)
            
            # Add progress information
            result["progress"] = f"{i + 1}/{total_chunks}"
            result["percent_complete"] = ((i + 1) / total_chunks) * 100
            
            # Stream the result for this chunk
            yield result
            
            # Simulate processing time
            time.sleep(1)

        # Send final completion message
        yield {
            "status": "completed",
            "total_chunks_processed": total_chunks,
            "final_timestamp": time.strftime("%H:%M:%S")
        }

    except Exception as e:
        yield {"error": str(e)}

# Start the serverless function with streaming enabled
runpod.serverless.start({
    "handler": aloha_sim_handler,
    "return_aggregate_stream": True
})