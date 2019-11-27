clear
clc

m = 1:10

y_1 = m.^m./factorial(m)

y_2 = []
for k = 1:10
    y_2_value = 0
    for n = 0:k-1
        y_2_value = y_2_value + k^n/factorial(n)
    end
    y_2 = [y_2 y_2_value]
end
pm = 1./(1+y_2./y_1)

u = [1 0.5 0.2]

y_3 = pm + 1/u(3)

plot(m,y_3)

title('u = 20%')

xlabel('number of M')

ylabel('y_3')