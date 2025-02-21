import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import styled from 'styled-components';

const Container = styled.div`
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: calc(100vh - 70px);
  padding: 20px;
`;

const Form = styled.form`
  width: 100%;
  max-width: 400px;
  padding: 32px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
`;

const Title = styled.h1`
  font-family: 'Mulish', sans-serif;
  font-size: 24px;
  color: #232833;
  margin-bottom: 24px;
  text-align: center;
`;

const Input = styled.input`
  width: 100%;
  height: 40px;
  padding: 0 12px;
  margin-bottom: 16px;
  border: 1px solid #008EDE24;
  border-radius: 4px;
  font-family: 'Mulish', sans-serif;
`;

const Button = styled.button`
  width: 100%;
  height: 40px;
  background: #008EDE;
  color: white;
  border: none;
  border-radius: 4px;
  font-family: 'Mulish', sans-serif;
  font-weight: 600;
  cursor: pointer;

  &:disabled {
    background: #008EDE50;
    cursor: not-allowed;
  }
`;

const StyledLink = styled(Link)`
  display: block;
  text-align: center;
  color: #008EDE;
  text-decoration: none;
  font-family: 'Mulish', sans-serif;
  font-size: 14px;
  margin-bottom: 16px;
`;

const SignUp = () => {
  const [formData, setFormData] = useState({
    login: '',
    email: '',
    password: ''
  });
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);

    try {
      const response = await fetch('/api/users/create_user', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      if (response.ok) {
        navigate('/login');
      } else {
        const error = await response.json();
        alert(error.detail);
      }
    } catch (error) {
      alert('Error creating account');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Container>
      <Form onSubmit={handleSubmit}>
        <StyledLink to="/login">Войти в аккаунт</StyledLink>
        <Title>Регистрация</Title>
        <Input
          type="text"
          placeholder="Логин"
          value={formData.login}
          onChange={(e) => setFormData({...formData, login: e.target.value})}
          required
        />
        <Input
          type="email"
          placeholder="Email"
          value={formData.email}
          onChange={(e) => setFormData({...formData, email: e.target.value})}
          required
        />
        <Input
          type="password"
          placeholder="Пароль"
          value={formData.password}
          onChange={(e) => setFormData({...formData, password: e.target.value})}
          required
        />
        <Button type="submit" disabled={isLoading}>
          {isLoading ? 'Загрузка...' : 'Зарегистрироваться'}
        </Button>
      </Form>
    </Container>
  );
};

export default SignUp; 