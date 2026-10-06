n <- 6

num_vec <- vector(mode = "numeric", length = n)
print("Numeric Vector:")
print(num_vec)
cat("Type:", typeof(num_vec), "| Length:", length(num_vec), "\n\n")

comp_vec <- vector(mode = "complex", length = n)
print("Complex Vector:")
print(comp_vec)
cat("Type:", typeof(comp_vec), "| Length:", length(comp_vec), "\n\n")

log_vec <- vector(mode = "logical", length = n)
print("Logical Vector:")
print(log_vec)
cat("Type:", typeof(log_vec), "| Length:", length(log_vec), "\n\n")

char_vec <- vector(mode = "character", length = n)
print("Character Vector:")
print(char_vec)
cat("Type:", typeof(char_vec), "| Length:", length(char_vec), "\n\n")