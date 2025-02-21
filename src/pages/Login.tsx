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
  margin-bottom: 16px;

  &:disabled {
    background: #008EDE50;
    cursor: not-allowed;
  }
`;

const ForgotPassword = styled(Link)`
  display: block;
  text-align: center;
  color: #008EDE;
  text-decoration: none;
  font-family: 'Mulish', sans-serif;
  font-size: 14px;
`;

const Login = () => {
  const [formData, setFormData] = useState({
    email: '',
    password: ''
  });
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);

    try {
      const response = await fetch('/api/auth/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      if (response.ok) {
        const data = await response.json();
        localStorage.setItem('token', data.access_token);
        navigate('/recommendations');
      } else {
        const error = await response.json();
        alert(error.detail);
      }
    } catch (error) {
      alert('Error logging in');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Container>
      <Form onSubmit={handleSubmit}>
        <Title>Вход</Title>
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
          {isLoading ? 'Загрузка...' : 'Войти'}
        </Button>
        <ForgotPassword to="/reset-password">Забыли пароль?</ForgotPassword>
      </Form>
    </Container>
  );
};

export default Login; 