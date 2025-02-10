(define pi 3.14)
(define e 2.71)
(define l '(((28 93 21) ((56 32))) ((((48) 53))) (((32))) 49 64))
(define (sum x y) (+ x y))

(define (factorial n)
    (if (= n 0) 1 
    (* n (factorial (- n 1)))
    )
)

(define (fibonnaci n)
    (cond 
        ((= n 1) 1)
        ((= n 2) 1)
        (else (+ (fibonnaci (- n 1)) (fibonnaci (- n 2))))
    )
)

(define (triple l)
    (cond 
        ((null? l) l)
        (else
            (append (list (* 3 (car l))) (triple (cdr l)))
        )
    )
)

(define (reverse l)
    (cond
        ((null? l) l)
        (else
            (append (reverse (cdr l)) (list (car l)))
        )
    )
)

(define (flatten l)
    (cond
        ((not (list? l)) (list l))
        ((null? l) l)
        (else
            (append (flatten (car l)) (flatten (cdr l)))
        )
    )
)



(define (merge l1 l2)
    (cond
        ((null? l1) l2)
        ((null? l2) l1)
        (else
            (if (< (car l1) (car l2)) 
                (append (list (car l1)) (merge (cdr l1) l2)) 
                (append (list (car l2)) (merge l1 (cdr l2)))
            )
        )
    )
)
(define (prefix-of-list l k)
    (cond
        ((= k 0) '())
        ((null? l) '())
        (else
            (append (list (car l)) (prefix-of-list (cdr l) (- k 1)))
        )
    )
)
(define (suffix-of-list l k)
    (reverse (prefix-of-list (reverse l) k))
)
(define (mergesort l)
    (cond
        ((<= (length l) 1) l)
        (else
            (merge
                (mergesort (prefix-of-list l (quotient (length l) 2)))
                (mergesort (suffix-of-list l (- (length l) (quotient (length l) 2))))
            )
        )
    )
)

(define (flatten-list l)
    (cond
        ((not (list? l)) (list l))
        ((null? l) l)
        (else
            (apply append (map flatten-list l))
        )
    )
)