def read_board(filename):
    try:
        with open(filename, 'r') as file:
            # Wczytaj pierwszą linię z wymiarami
            w, k = map(int, file.readline().split())
            
            # Wczytaj planszę
            board = []
            for _ in range(w):
                # Wczytaj linię, podziel na liczby i przekonwertuj na int
                row = list(map(int, file.readline().split()))
                if len(row) != k:
                    raise ValueError("Nieprawidłowa liczba elementów w wierszu")
                board.append(row)
            
            # Sprawdź czy jest dokładnie jedno zero
            zero_count = sum(row.count(0) for row in board)
            if zero_count != 1:
                raise ValueError("Układanka musi zawierać dokładnie jedno pole puste (0)")
                
            return board
            
    except FileNotFoundError:
        print(f"Błąd: Plik '{filename}' nie został znaleziony")
        return None
    except ValueError as e:
        print(f"Błąd: {str(e)}")
        return None